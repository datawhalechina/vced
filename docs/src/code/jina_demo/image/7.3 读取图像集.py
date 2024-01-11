from jina import DocumentArray

da = DocumentArray.from_files('Downloads/*.jpg')  # 从Downloads文件夹中读取所有的jpg文件，在这里你应该根据自己的路径设置
da.plot_image_sprites('sprite-img.png')  # 使用 plot_image_sprites 绘制图片集图片，如下图

