# VideoLoader

## 基础实现

### YAML配置


```yaml
jtype: VideoLoader
metas:
  py_modules:
    - video_loader.py
```

### 导入第三方库

```python
import io
import os
import random
import re
import string
import tempfile
import urllib.request
import urllib.parse
from copy import deepcopy
from typing import Dict, Iterable, Optional
from pathlib import Path

import ffmpeg
import librosa
import numpy as np
import webvtt
from jina import Executor, requests
from docarray import Document, DocumentArray
from jina.logging.logger import JinaLogger
from PIL import Image
import math
import 
```

### 默认设置
=======
## 介绍

```python
DEFAULT_FPS = 1.0
DEFAULT_AUDIO_BIT_RATE = 160000
DEFAULT_AUDIO_CHANNELS = 2
DEFAULT_AUDIO_SAMPLING_RATE = 44100
DEFAULT_SUBTITLE_MAP = '0:s:0'
```

参数解释：

+ `DEFAULT_FPS`：默认视频每秒传输帧数（此处视频截取精度为1s）
+ `DEFAULT_AUDIO_BIT_RATE`：默认音频比特率（码率）
+ `DEFAULT_AUDIO_CHANNELS`：默认音频通道数
+ `DEFAULT_AUDIO_SAMPLING_RATE`：默认音频采样率
+ `DEFAULT_SUBTITLE_MAP`：默认第一路字幕文件输出流，详情参见[FFmpeg使用基础](https://www.ai2news.com/blog/1729893/)

### 类初始化

```python
class VideoLoader(Executor):

    def __init__(
        self,
        modality_list: Iterable[str] = ('image', 'audio', 'text'),
        ffmpeg_video_args: Optional[Dict] = None,
        ffmpeg_audio_args: Optional[Dict] = None,
        ffmpeg_subtitle_args: Optional[Dict] = None,
        librosa_load_args: Optional[Dict] = None,
        copy_uri: bool = True,
        **kwargs,
    ):

        super().__init__(**kwargs)
```

参数解释：

+ `modality_list`：需要提取的不同模态数据类型
+ `ffmpeg_video_args`：视频抽帧所需确定的参数
+ `ffmpeg_audio_args`：音频抽取所需确定的参数
+ `ffmpeg_subtitle_args`：字幕抽取所需确定的参数
+ `librosa_load_args`：将音频数据转换成张量所需确定的参数
+ `copy_uri`：是否存储视频对应`uri`

```python
        self._modality = modality_list
        self._copy_uri = copy_uri
```

````python
        self._ffmpeg_video_args = ffmpeg_video_args or {}
        self._ffmpeg_video_args.setdefault('format', 'rawvideo')
        self._ffmpeg_video_args.setdefault('pix_fmt', 'rgb24')
        self._ffmpeg_video_args.setdefault('frame_pts', True)
        self._ffmpeg_video_args.setdefault('vsync', 0)
        self._ffmpeg_video_args.setdefault('vf', f'fps={DEFAULT_FPS}')
        fps = re.findall('.*fps=(\d+(?:\.\d+)?).*', self._ffmpeg_video_args['vf'])
        if len(fps) > 0:
            self._frame_fps = float(fps[0])
````

视频相关参数设定

```python
        self._ffmpeg_audio_args = ffmpeg_audio_args or {}
        self._ffmpeg_audio_args.setdefault('format', 'wav')
        self._ffmpeg_audio_args.setdefault('ab', DEFAULT_AUDIO_BIT_RATE)
        self._ffmpeg_audio_args.setdefault('ac', DEFAULT_AUDIO_CHANNELS)
        self._ffmpeg_audio_args.setdefault('ar', DEFAULT_AUDIO_SAMPLING_RATE)

        self._ffmpeg_subtitle_args = ffmpeg_subtitle_args or {}
        self._ffmpeg_subtitle_args.setdefault('map', DEFAULT_SUBTITLE_MAP)
```

音频相关参数设定

```python
        self._librosa_load_args = librosa_load_args or {}
        self._librosa_load_args.setdefault('sr', self._ffmpeg_audio_args['ar'])
        self._librosa_load_args.setdefault('mono', self._ffmpeg_audio_args['ac'] > 1)
```

字幕相关参数设定

```python
        self.logger = JinaLogger(
            getattr(self.metas, 'name', self.__class__.__name__)
        ).logger
```


导入日志信息类

### 视频抽取

@requests方法可以参考[官网说明](https://docs.jina.ai/concepts/executor/add-endpoints/?utm_campaign=vced&utm_source=github&utm_medium=datawhale)

参数解释：

+ `docs`：包含了 [Document](https://docarray.jina.ai/fundamentals/document/?utm_campaign=vced&utm_source=github&utm_medium=datawhale)  的待编码的  [DocumentArray](https://docarray.jina.ai/fundamentals/documentarray/?utm_campaign=vced&utm_source=github&utm_medium=datawhale) 
+ `parameters`：字典类型，包含了用于控制编码的参数（keys包括`traversal_paths`和`batch_size`)
```Python
# In Jina 添加到flow中
from jina import Flow
from docarray import Document, DocumentArray


```python
    @requests(on='/extract')
    def extract(self, docs: DocumentArray, parameters: Dict, **kwargs):
        t1 = time.time()
        print('video_loader extract', t1)
        for doc in docs:
            print(f'video chunks: {len(doc.chunks)}')
        for doc in docs:
            self.logger.info(f'received {doc.id}')

            if doc.uri == '':
                self.logger.error(f'No uri passed for the Document: {doc.id}')
                continue

            with tempfile.TemporaryDirectory() as tmpdir:
                source_fn = (
                    self._save_uri_to_tmp_file(doc.uri, tmpdir)
                    if self._is_datauri(doc.uri)
                    else doc.uri
                )

```


读入视频文件

```python
                if 'image' in self._modality:
                    ffmpeg_video_args = deepcopy(self._ffmpeg_video_args)
                    ffmpeg_video_args.update(parameters.get('ffmpeg_video_args', {}))
                    frame_tensors = self._convert_video_uri_to_frames(
                        source_fn, doc.uri, ffmpeg_video_args
                    )
                    for idx, frame_tensor in enumerate(frame_tensors):
                        self.logger.debug(f'frame: {idx}')
                        chunk = Document(modality='image')
                        max_size = 240
                        img = Image.fromarray(frame_tensor)
                        if img.size[0] > img.size[1]:
                            width = max_size
                            height = math.ceil(max_size / img.size[0] * img.size[1])
                        else:
                            height = max_size
                            width = math.ceil(max_size / img.size[1] * img.size[0])
                        img = img.resize((width, height))
                        chunk.tensor = np.asarray(img).astype('uint8')
                        print(chunk.tensor.shape)
                        # chunk.tensor = np.array(frame_tensor).astype('uint8')
                        chunk.location = (np.uint32(idx),)
                        chunk.tags['timestamp'] = idx / self._frame_fps
                        if self._copy_uri:
                            chunk.tags['video_uri'] = doc.uri
                        doc.chunks.append(chunk)
                        
            t2 = time.time()
            print(t2 - t1, t2)
       
```

将图片转换为张量

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

### 图片参数获取

```python
    def _convert_video_uri_to_frames(self, source_fn, uri, ffmpeg_args):
        video_frames = []
        try:
            video = ffmpeg.probe(source_fn)['streams'][0]
            w, h = ffmpeg_args.get('s', f'{video["width"]}x{video["height"]}').split('x')
            w = int(w)
            h = int(h)
            out, _ = (
                ffmpeg.input(source_fn)
                .output('pipe:', **ffmpeg_args)
                .run(capture_stdout=True, quiet=True)
            )
            video_frames = np.frombuffer(out, np.uint8) #.reshape([-1, h, w, 3])
            video_frames = video_frames.reshape([-1, h, w, 3])

        except ffmpeg.Error as e:
            self.logger.error(f'Frame extraction failed, {uri}, {e.stderr}')

        return video_frames
```

获取视频中图片的width和height

### 音频参数获取

```python
    def _convert_video_uri_to_audio(self, source_fn, uri, ffmpeg_args, librosa_args):
        data = None
        sample_rate = None
        try:
            out, _ = (
                ffmpeg.input(source_fn)
                .output('pipe:', **ffmpeg_args)
                .run(capture_stdout=True, quiet=True)
            )
            data, sample_rate = librosa.load(io.BytesIO(out), **librosa_args)
        except ffmpeg.Error as e:
            self.logger.error(
                f'Audio extraction failed with ffmpeg, uri: {uri}, {e.stderr}'
            )
        except librosa.LibrosaError as e:
            self.logger.error(f'Array conversion failed with librosa, uri: {uri}, {e}')
        finally:
            return data, sample_rate
```

获取视频中音频采样率

### 字幕数据获取

```python
    def _convert_video_uri_to_subtitle(self, source_fn, ffmpeg_args, tmp_dir):
        subtitle_fn = str(os.path.join(tmp_dir, 'subs.srt'))
        subtitles = []
        print(ffmpeg_args)
        try:
            out, _ = (
                ffmpeg.input(source_fn)
                .output(subtitle_fn, **ffmpeg_args)
                .run(capture_stdout=True, quiet=True)
            )
            subtitles = self._process_subtitles(Path(subtitle_fn))
        except ffmpeg.Error as e:
            self.logger.error(f'Subtitle extraction failed with ffmpeg, {e.stderr}')
        finally:
            return subtitles
```

获取视频中处理过的字幕文本

```python
    def _process_subtitles(
        self, srt_path: Path, vtt_path: Path = None, tmp_srt_path: Path = None
    ):
        beg = None
        is_last_cap_complete = True
        subtitles = []
        prev_parts = []
        vtt_fn = self._convert_srt_to_vtt(srt_path, vtt_path, tmp_srt_path)
        for caption in webvtt.read(vtt_fn):
            cur_parts = [
                t
                for t in filter(lambda x: len(x.strip()) > 0, caption.text.split('\n'))
            ]
            filtered_text = ' '.join(cur_parts)
            if len(cur_parts) == 1:
                if cur_parts[0] in prev_parts:
                    continue
            if len(cur_parts) > 1:
                if cur_parts[0] in prev_parts and is_last_cap_complete:
                    filtered_text = ' '.join(cur_parts[1:])
            is_cur_complete = True
            if is_last_cap_complete:
                beg = caption.start_in_seconds
            if caption.text.startswith(' \n') or caption.text.endswith('\n '):
                is_cur_complete = False
            if is_cur_complete:
                if filtered_text:
                    subtitles.append((beg, caption.end_in_seconds, filtered_text))
            is_last_cap_complete = is_cur_complete
            prev_parts = cur_parts
        return subtitles
```

对字幕按照换行情况进行切分

```python
    def _remove_carriage_return(self, input_path, output_path=None):
        result = []
        with open(input_path, 'rb') as f:
            for l in f:
                if l == b'\r\n':
                    continue
                new_l = l.decode('utf8').replace('\r\n', '\n')
                new_l = new_l.rstrip('\n')
                result.append(new_l)
        if output_path is None:
            output_fn = f'{input_path.stem}_no_cr{input_path.suffix}'
            output_path = input_path.parent / output_fn
        with open(output_path, 'w') as f:
            f.write('\n'.join(result))
        return output_path
```

除去所有回车

```python
    def _convert_srt_to_vtt(
        self, srt_path: Path, vtt_path: Path = None, tmp_srt_path: Path = None
    ):
        if vtt_path is None:
            vtt_path = srt_path.parent / f'{srt_path.stem}.vtt'
        try:
            result = webvtt.from_srt(srt_path)
        except webvtt.errors.MalformedCaptionError as e:
            self.logger.warning('remove carriage returns from the .srt file')
            srt_path = self._remove_carriage_return(srt_path, tmp_srt_path)
            result = webvtt.from_srt(srt_path)
        result.save(output=vtt_path)
        return vtt_path
```

将srt字幕文件转换为webvtt字幕文件

### 其他

```python
    def _save_uri_to_tmp_file(self, uri, tmpdir):
        req = urllib.request.Request(uri, headers={'User-Agent': 'Mozilla/5.0'})
        tmp_fn = os.path.join(
            tmpdir,
            ''.join([random.choice(string.ascii_lowercase) for i in range(10)])
            + '.mp4',
        )
        with urllib.request.urlopen(req) as fp:
            buffer = fp.read()
            binary_fn = io.BytesIO(buffer)
            with open(tmp_fn, 'wb') as f:
                f.write(binary_fn.read())
        return tmp_fn
```

文件写入

```python
    def _is_datauri(self, uri):
        scheme = urllib.parse.urlparse(uri).scheme
        return scheme in {'data'}
```
=======
## 示例


判别是否为已有uri

## 进阶延展

### Executor 调用

多数用户可以想到的功能都已经被上传到 [Executor Hub](https://cloud.jina.ai/executors?utm_campaign=vced&utm_source=github&utm_medium=datawhale) 上，VideoLoader 的 [Executor](https://cloud.jina.ai/executor/i6gp4vwu?utm_campaign=vced&utm_source=github&utm_medium=datawhale) 也可以在 Executor hub 中进行访问，可以直接调用封装好的 Executor，实现自己的功能模块。

### flow配置

```YAML
executors:
	- name : loader
	  uses: 'jinahub://VideoLoader/latest'
```