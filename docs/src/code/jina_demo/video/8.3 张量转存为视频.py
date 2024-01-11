# 使用 save_video_tensor_to_file 进行视频的保存
from docarray import Document

d = (
    Document(uri='cat.mp4')
    .load_uri_to_video_tensor()  # 读取视频
    .save_video_tensor_to_file('60fps.mp4', 60)  # 将其保存为60fps的视频
)
