# CustomClipText

## 基础实现

### YAML配置

```yaml
jtype: CLIPTextEncoder
metas:
  py_modules:
    - clip_text.py
```

### 导入第三方库

```python
from typing import Dict, Optional

import torch
from docarray import DocumentArray
from jina import Executor, requests
import clip
import time
```

### 类初始化

```python
class CLIPTextEncoder(Executor):

    def __init__(
        self,
        pretrained_model_name_or_path: str = 'ViT-B/32',
        base_tokenizer_model: Optional[str] = None,
        max_length: int = 77,
        device: str = 'cpu',
        traversal_paths: str = '@r',
        batch_size: int = 32,
        *args,
        **kwargs,
    ):
        
        super().__init__(*args, **kwargs)
```

参数解释：

+ `pretrained_model_name_or_path`：可以是 [Hugging Face](https://huggingface.co/) 中的线上 repository，亦或是本地的 directory，此处预训练的模型使用 Vision Transformer-Base/32, input batch size 为 32*32
+ `base_tokenizer_model`：基础的分词器，如果为空值的话则默认使用 `pretrained_model_name_or_path`
+ `max_length`：分词器能接受的最大长度，所有CLIP模型都为77
+ `device`：预处理设备
+ `traversal_paths`：遍历路径
+ `batch_size`：批大小

```python
        self.traversal_paths = traversal_paths
        self.batch_size = batch_size
        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.base_tokenizer_model = (
            base_tokenizer_model or pretrained_model_name_or_path
        )
```

此处即上述`base_tokenizer_model`所取的或逻辑

```python
        self.max_length = max_length

        self.device = device

        model, preprocessor = clip.load(self.pretrained_model_name_or_path, device=device)
        
        self.preprocessor = preprocessor
        self.model = model
```

### 文本编码

```python
    @requests
	def encode(self, docs: DocumentArray, parameters: Dict, **kwargs):
        print('clip_text encode')
        for docs_batch in DocumentArray(
            filter(
                lambda x: bool(x.text),
                docs[parameters.get('traversal_paths', self.traversal_paths)],
            )
        ).batch(batch_size=parameters.get('batch_size', self.batch_size)) :
            text_batch = docs_batch.texts
```

参数解释：

+ `docs`：包含了 Documents 的待编码的 DocumentArray
+ `parameters`：字典类型，包含了用于控制编码的参数（keys 包括 `traversal_paths` 和 `batch_size`)

对数据类型进行过滤，对所有文本进行批处理

```python
            t1 = time.time()
            with torch.inference_mode():
                input_tokens = [self.model.encode_text(clip.tokenize([t, "unknown"]).to(self.device)) for t in text_batch]
                embeddings = input_tokens
                for doc, embedding in zip(docs_batch, embeddings):
                    doc.embedding = embedding
            t2 = time.time()
            print("encode text cost:", t2 - t1)
            print(t1)
            print(t2)
```

对文本数据进行编码，以 DocumentArray 形式存储，便于后续传值