from jina import Document

d = Document(uri='complicated-image.jpeg')
d.load_uri_to_image_tensor()
print(d.tensor.shape)  # (792, 1000, 3)

d.convert_image_tensor_to_sliding_windows(window_shape=(64, 64))  # 使用 64*64 的滑窗切割原图像，切分出 13*16=208 个图像张量
print(d.tensor.shape)  # (208, 64, 64, 3)

# 可以通过 as_chunks=True，使得上述 208 张图片张量添加到 Document 块中。
# PS：运行这行代码时，需要重新 load image tensor，否则会报错。
d = Document(uri='complicated-image.jpeg')
d.load_uri_to_image_tensor()
d.convert_image_tensor_to_sliding_windows(window_shape=(64, 64), as_chunks=True)
print(d.chunks)

d.chunks.plot_image_sprites('simpsons-chunks.png')  # 使用 plot_image_sprites 将各个 chunk 绘制成图片集图片

# 因为采用了滑动窗口扫描整个图像，使用了默认的 stride，切分后的图像不会有重叠，所以重新绘制出的图和原图差别不大。
# 你也可以通过设置 strides 参数进行过采样。
d.convert_image_tensor_to_sliding_windows(window_shape=(64, 64), strides=(10, 10), as_chunks=True)
d.chunks.plot_image_sprites('simpsons-chunks-stride-10.png')
