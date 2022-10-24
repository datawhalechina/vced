# 视频需要依赖 av 包
# pip install av
from jina import Document

d = Document(uri='cat.mp4')
d.load_uri_to_video_tensor()

# 相较于图像，视频是一个 4 维数组，第一维表示视频帧 id 或是视频的时间，剩下的三维则和图像一致。
print(d.tensor.shape)  # (31, 1080, 1920, 3)

# 使用 append 方法将 Document 放入 chunk 中
for b in d.tensor:
    d.chunks.append(Document(tensor=b))

d.chunks.plot_image_sprites('mov.png')
