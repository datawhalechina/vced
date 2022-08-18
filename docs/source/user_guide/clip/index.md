# Clip 简介
clip 

## 一.原理介绍
### 1.CV模型
&ensp;&ensp;先从简单的CV模型VGG说起，VGG模型将多个块进行堆叠，实现了当时人脸识别state of the 
art的结果。后续一些有关研究神经网络模型层间特征图可视化的工作表明，涉及计算机视觉
分类的模型更多的依赖于模型
末端的神经层。也就是说，越靠近输出的神经网络层越具有任务相关性。这种结果也同样在NL
P第三范式：pre-trained + fine tune。语言模型在大规模语料上进行预训练之后，便具有了强大的语义表征能力。实验证明(bert)，将PLM接上后续任务相关神经网络层进行微调，可以在下游任务上达到更好的表现。  
&ensp;&ensp;同样，在CV深度神经网络中，通过可视化的方法，也可以发现，模型最前端的神经网络层倾向
于提取一些普遍的、共有的视觉特征，如纹理、边缘等信息。
越往后则越倾向于任务相关的特征。也就是说，模型在某种程度上具有了提取普遍特征的能力。  
### 2.对比学习
&ensp;&ensp;这里先说说对比学习。一般情况下，倘若我们要对猫狗二分类，一个简单的想法就是对其分
别打上对应的标签，进行分析学习。同时，我们也可以通过对比学习的方法来实现，简单来说，就是不再将所有的猫（或狗）照片通过神经网络分别映射到对应标签，而是让经过神经网络处理之后原属同一类别的特征向量之间的距离尽可能接近，让原
本不属于同一类别的特征向量之间的距离尽可能拉远。这就有点聚类的感觉，但是还是有监督信号的。  
### 3.NLP模型
&ensp;&ensp;下面引出语言模型的介绍。bert，gpt系列的模型离不开transformer模型的发明。自注意
力机制更好的捕获了数据间的关系。较为人知的NLP模型是bert模型。
bert模型的预训练任务主要为模拟人的完形填空任务，在这种预训练方法下，模型需要同时
关注上下文间的信息，从而推理得出当前位置的token。另一种非常强的NLP模型：gpt，则
使用了自回归的方法来训练，也就是说，模型仅可通过当前位置之前的字段来推理当前位置
的token。在这之后，unilm模型将两种注意力模型联合起来进行训练。encoder-decoder
是NLP领域普遍使用的框架，但这块内容与multi modal部分关系不大，再次不过多赘述。
如果我们能够将图像信息和语义信息（或者其他模态的信息）映射到同一空间后，再进行训
练，那么在某种程度上，模型可以在多种模态之间建立联系。
### 4.多模态模型
clip(contrastive language image pre train)将语言信息和图像信息联合训练，实现
了在下游任务上zero shot的能力。  
&ensp;&ensp;具体来说，clip将图像的分类任务转化为了图文匹配的任务，更一步，就是通过将图像信息
和语义信息映射到同一多模态语义空间下，再使用对比学习的方法进行训练。具体细节可参
考论文：[Learning transferable visual models from natural language supervision](https://arxiv.org/pdf/2103.00020.pdf)  
下面对clip模型结合jina框架进行相关代码介绍。  
在本项目中，我们将clip模型封装成Executor，最后将其作为微服务嵌入Flow中调用。  
## 二.代码介绍
### 1.图像Executor
```python
class CLIPImageEncoder(Executor):
    """Encode image into embeddings using the CLIP model."""

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
        self.batch_size = batch_size
        self.traversal_paths = traversal_paths
        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.logger = JinaLogger(self.__class__.__name__)
        self.device = device
        model, preprocessor = clip.load(self.pretrained_model_name_or_path, device=device)
        self.preprocessor = preprocessor
        self.model = model
    @requests
    def encode(self, docs: DocumentArray, parameters: dict, **kwargs):
        document_batches_generator =  DocumentArray(
            filter(
                lambda x: x is not None,
                docs[parameters.get('traversal_paths', self.traversal_paths)],
            )
        ).batch(batch_size=parameters.get('batch_size', self.batch_size))
        with torch.inference_mode():
            for batch_docs in document_batches_generator:
                for d in batch_docs:
                    tensors_batch = []
                    for c in d.chunks:
                        if (c.modality == 'image'):
                            image_embedding = self.model.encode_image(self.preprocessor(Image.fromarray(c.tensor)).unsqueeze(0).to(self.device))
                            tensors_batch.append(np.array(image_embedding).astype('float32'))
                    embedding = tensors_batch
                    d.embedding = embedding
```
详细代码可在项目文件夹中找到。  
上述为jina框架对模型的一个简单分装，对其他模型而言，其分装流程大体相同。具体来说，就是加载模型，并将end point与encode函数绑定即可。
在代码的`__init__`函数部分，我们加载了模型，并设定了相关参数和组件，如batch_size，device等等。
`encode`函数是Executor的核心部分，它将Document中的信息进行编码，并将编码后得到的向量存入Document.embedding中。

### 2.文本编码Executor

```python
class CLIPTextEncoder(Executor):
    """Encode text into embeddings using the CLIP model."""

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
        self.traversal_paths = traversal_paths
        self.batch_size = batch_size
        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.base_tokenizer_model = (
            base_tokenizer_model or pretrained_model_name_or_path
        )
        self.max_length = max_length
        self.device = device
        model, preprocessor = clip.load(self.pretrained_model_name_or_path, device=device)
        self.preprocessor = preprocessor
        self.model = model

    @requests
    def encode(self, docs: DocumentArray, parameters: Dict, **kwargs):
        for docs_batch in DocumentArray(
            filter(
                lambda x: bool(x.text),
                docs[parameters.get('traversal_paths', self.traversal_paths)],
            )
        ).batch(batch_size=parameters.get('batch_size', self.batch_size)) :
            text_batch = docs_batch.texts
            with torch.inference_mode():
                input_tokens = [self.model.encode_text(clip.tokenize([t, "unknown"]).to(self.device)) for t in text_batch] 
                embeddings = input_tokens
                for doc, embedding in zip(docs_batch, embeddings):
                    doc.embedding = embedding
```
负责处理文本的Executor的实现逻辑与处理图像的Executor的实现逻辑类似。即，先加载模型，配置参数和前置处理流程，之后再编写encode函数：调用模型对图像或文本进行编码，并将其与end point绑定。这里代码的区别就是对图像模型和文本模型本身的调用方式。

在使用Executor时，我们可以使用`config.yml`文件进行配置，主要为EXecutor相关的一些参数的设定。在这种模式下，我们只需要修改配置文件，而不需要修改代码，便可实现在多种场景下应用下的灵活切换。
## 三.配置使用

```yml
jtype: CLIPTextEncoder
metas:
  py_modules:
    - clip_text.py

```






```{toctree}
:caption: clip

clip-as-service
```