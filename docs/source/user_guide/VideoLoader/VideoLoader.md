# VideoLoader

[VideoLoader | latest | Jina Hub](https://hub.jina.ai/executor/i6gp4vwu)

使用`ffmpeg`从视频中提取图像帧、音频和字幕的执行器



## 介绍

`VideoLoader` [executor](https://docs.jina.ai/fundamentals/executor/) 帮助将视频组件加载到Jina的 [`Document`](https://docs.jina.ai/fundamentals/document/) 类型中。它使用[`ffmpeg-python`](https://github.com/kkroening/ffmpeg-python)从视频中提取**图像帧、音频和字幕**。

提取的图像帧、音频和字幕存储为具有以下属性的 `chunks` 块

图像帧块具有图像模式，音频块具有音频模式，字幕块具有文本模式。在字幕解析期间，重复的字幕被合并，以启发式方式形成独特的字幕，并作为单个块返回，并在标签中具有各自的开始和结束时间。

| data         | stored in                | `modality` | `location`                             | `tags`                                                       |
| :----------- | :----------------------- | :--------- | :------------------------------------- | :----------------------------------------------------------- |
| image frames | `blob` (dtype=`uint8`)   | `image`    | the index of the frame                 | `{'timestampe': 0.5}`, the timestamp of the frame in seconds. `{'video_uri': 'video.mp4'}`, the uri of the video |
| audio        | `blob` (dtype=`float32`) | `audio`    | N/A                                    | `{'sample_rate': 140000}`, the sample rate of the audio. `{'video_uri': 'video.mp4'}`, the uri of the video. |
| subtitle     | `text` (dtype=`str`)     | `text`     | the index of the subtitle in the video | `{'beg_in_seconds': 0.5}`, the beginning of a caption in seconds, `{'end_in_seconds': 0.6}`, the end of a caption in seconds. `{'video_uri': 'video.mp4'}`, the uri of the video. |



## 构造函数参数

| Kwarg                | Type                       | Default        | Description                                                  |
| :------------------- | :------------------------- | :------------- | :----------------------------------------------------------- |
| modality_list        | ('image', 'audio', 'text') | Iterable[str]  | the data from different modalities to be extracted. By default, `modality_list=('image', 'audio')`, both image frames and audio track are extracted. |
| ffmpeg_video_args    | None                       | Optional[Dict] | the arguments to `ffmpeg` for extracting frames. By default, `format='rawvideo'`, `pix_fmt='rgb24`, `frame_pts=True`, `vsync=0`, `vf=[FPS]`, where the frame per second(FPS)=1. The width and the height of the extracted frames are the same as the original video. To reset width=960 and height=540, use `ffmpeg_video_args={'s': '960x540'`}. |
| ffmpeg_audio_args    | None                       | Optional[Dict] | the arguments to `ffmpeg` for extracting audios. By default, the bit rate of the audio `ab=160000`, the number of channels `ac=2`, the sampling rate `ar=44100` |
| ffmpeg_subtitle_args | None                       | Optional[Dict] | the arguments to `ffmpeg` for extracting subtitle. By default, we extract the first subtitle by setting `map='0:s:0'`. To extract second subtitle in a video use `ffmpeg_subtitle_args{map='0:s:1'}` and so on. |
| librosa_load_args    | None                       | Optional[Dict] | the arguments to `librosa.load()` for converting audio data into `tensor`. By default, the sampling rate (`sr`) is the same as in `ffmpeg_audio_args['ar']`, the flag for converting to mono (`mono`) is `True` when `ffmpeg_audio_args['ac'] > 1` |
| copy_uri             | True                       | bool           | Set to `True` to store the video `uri` at the `.tags['video_uri']` of the chunks that are extracted from the video. By default, `copy_uri=True`. Set this to `False` when the video uri is a data uri. |



## 代码

```Python
# In DocArray 请求API
from docarray import Document, DocumentArray

da = DocumentArray([Document(text='hello')])
r = da.post('jinahub://VideoLoader/latest')

print(r.to_json())
```



```Python
# In Jina 添加到flow中
from jina import Flow
from docarray import Document, DocumentArray

f = Flow().add(uses='jinahub://VideoLoader/latest', name='VideoLoader')

with f:
r = f.post('/', inputs=DocumentArray([Document(text='hello')]))
print(r.to_json())
```



## 示例

通过`VideoLoader`处理上传视频

![](images/video_loader.png)



处理后的结果保存为二进制内容

![](images/result_binary_data.png)