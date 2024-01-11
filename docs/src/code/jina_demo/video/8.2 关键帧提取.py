from docarray import Document

d = Document(uri='cat.mp4')
# 可以使用 only_keyframes 这个参数来提取关键帧
d.load_uri_to_video_tensor(only_keyframes=True)
print(d.tensor.shape)  # (2, 1080, 1920, 3)
