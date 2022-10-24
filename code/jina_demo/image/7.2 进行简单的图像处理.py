from jina import Document

d = (
    Document(uri='apple.png')
    .load_uri_to_image_tensor()
    .set_image_tensor_shape(shape=(224, 224))  # 设置shape
    .set_image_tensor_normalization()  # 标准化
    .set_image_tensor_channel_axis(-1, 0)  # 更改通道
)

print(d.tensor.shape)  # (3, 224, 224)
print(d.tensor)

# 你可以使用 save_image_tensor_to_file 将 tensor 转为图像。当然，因为做了预处理，图片返回时损失了很多信息。
d.save_image_tensor_to_file('apple-proc.png', channel_axis=0)  # 因为前面进行了预处理，channel_axis应该设为0
