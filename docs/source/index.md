# VCED

VCED: Video Clip Extraction by description 可以通过你的文字描述来自动识别视频中相符合的片段进行视频剪辑。该项目基于跨模态搜索与向量检索技术搭建，通过前后端分离的模式，帮助你快速的接触新一代搜索技术。

## VCED 是如何工作的

VCED 项目的核心逻辑如下图所示

![CLIP](./_static/pic/CLIP.png)

- 首先将输入的文本通过 Text Encoder 进行 encoding
- 其次将上传的视频通过 Image Encoder 进行 encoding，一般上传的视频都会通过抽取关键帧的方式对内容进行提取，最终将上传的视频提取为多个图像
- 最终模型的目的是使文本生成的向量数据与抽取得到的图像的向量数据映射到同一高维空间下，并使得符合描述的向量距离尽可能的近
- 通过以上操作后再输入一段文本后就可以将生成的向量到原有的图像向量中进行搜索，找到最符合描述的图像后，再对原视频进行定位，最终找到相似的视频片段

所以为了实现以上几个步骤，在本项目中引入了以下组件：

- 为了解决如何对视频进行关键帧提取的问题，我们使用到了 ffmpeg，对应的实现方法在 [videoLoader](https://github.com/datawhalechina/vced/blob/709de9a0a0ce6a0b534c243c5bb58e00a08c6379/code/service/videoLoader/video_loader.py) 中
- 为了解决如何将文本与图像转换为向量的问题，我们使用到了 jina 的 DocArray，对应处理文本的方法在 [customClipText](https://github.com/datawhalechina/vced/blob/709de9a0a0ce6a0b534c243c5bb58e00a08c6379/code/service/customClipText/clip_text.py) 中，对应处理图像的方法在 [customClipImage](https://github.com/datawhalechina/vced/blob/709de9a0a0ce6a0b534c243c5bb58e00a08c6379/code/service/customClipImage/clip_image.py) 中
- 为了解决如何将生成的向量数据存储以及检索的问题，我们使用到了 jina 自带的向量搜索方法，对应的实现方法在 [customIndexer](https://github.com/datawhalechina/vced/blob/709de9a0a0ce6a0b534c243c5bb58e00a08c6379/code/service/customIndexer/executor.py) 中
- 为了解决前端显示的问题，我们使用到了 streamlit 框架实现前端效果，对应的实现方法在 [web/app.py](https://github.com/datawhalechina/vced/blob/709de9a0a0ce6a0b534c243c5bb58e00a08c6379/code/web/app.py) 中

在了解了本项目的逻辑后就让我们具体的来了解本项目中使用到的组件是如何使用的，最终帮助你实现一个类似的项目。

```{toctree}
:maxdepth: 2

user_guide/index
```
