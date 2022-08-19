# CustomClipImage

## 基础实现

### YAML配置

```yaml
jtype: CLIPImageEncoder
metas:
  py_modules:
    - clip_image.py
```

### 导入第三方库

```python
from typing import Optional, Tuple, Dict

import torch
from docarray import DocumentArray
from jina import Executor, requests
from jina.logging.logger import JinaLogger
from transformers import CLIPFeatureExtractor, CLIPModel
import numpy as np
import clip
from PIL import Image
import 
```

### 类初始化

```python
class CLIPImageEncoder(Executor):

    def __init__(
        self,
        pretrained_model_name_or_path: str = 'ViT-B/32',
        device: str = 'cpu',
        batch_size: int = 32,
        traversal_paths: str = '@r',
        *args,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
```

参数解释：

+ `pretrained_model_name_or_path`：可以是[Hugging Face](https://huggingface.co/)中的线上repository，亦或是本地的directory，此处预训练的模型使用Vision Transformer-Base/32, input batch size为32*32
+ `device`：预处理设备
+ `batch_size`：批大小
+ `traversal_paths`：遍历路径

```python
        self.batch_size = batch_size
        self.traversal_paths = traversal_paths
        self.pretrained_model_name_or_path = pretrained_model_name_or_path

        self.logger = JinaLogger(self.__class__.__name__)
```

导入日志信息类

```python
        self.device = device

        model, preprocessor = clip.load(self.pretrained_model_name_or_path, device=device)
        
        self.preprocessor = preprocessor
        self.model = model
```

### 图像编码

@requests方法可以参考[官网说明](https://docs.jina.ai/fundamentals/executor/executor-methods/?highlight=request%20method)

```python
    @requests
    def encode(self, docs: DocumentArray, parameters: dict, **kwargs):
        t1 = time.time()
        print('clip_image encode', t1)
        document_batches_generator =  DocumentArray(
            filter(
                lambda x: x is not None,
                docs[parameters.get('traversal_paths', self.traversal_paths)],
            )
        ).batch(batch_size=parameters.get('batch_size', self.batch_size))
```

参数解释：

+ `docs`：包含了Documents的待编码的DocumentArray
+ `parameters`：字典类型，包含了用于控制编码的参数（keys包括`traversal_paths`和`batch_size`)

对数据类型进行过滤，对所有图像进行批处理

```python
        with torch.inference_mode():
            for batch_docs in document_batches_generator:
                print('in for')
                for d in batch_docs:
                    print('in clip image d.uri', d.uri, len(d.chunks))
                    tensors_batch = []
                    for c in d.chunks:
                        if (c.modality == 'image'):
                            image_embedding = self.model.encode_image(self.preprocessor(Image.fromarray(c.tensor)).unsqueeze(0).to(self.device))
                            tensors_batch.append(np.array(image_embedding).astype('float32'))
                    embedding = tensors_batch
                    
                    d.embedding = embedding
        t2 = time.time()
        print('clip_image encode end', t2 - t1, t2)
```

通过URI访问图像数据，对其进行编码，以DocumentArray形式存储，便于后续传值

## 进阶延展

### Executor调用

多数用户可以想到的功能都已经被上传到[Jina Hub](https://hub.jina.ai/)上，CustomClipImage的[主体](https://hub.jina.ai/executor/0hnlmu3q)也可以在hub中进行访问，可以直接调用封装好的Executor，实现自己的功能模块，同时可以通过*latest-gpu*版本利用显存资源

### flow配置

```YAML
executors:
	- name : encoder
	  uses: 'jinahub://CLIPImageEncoder/latest'
	  timeout_ready : -1
	  uses_with:
	  	name: openai/clip-vit-base-patch32
```