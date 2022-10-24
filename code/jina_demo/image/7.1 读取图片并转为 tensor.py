from jina import Document

d = Document(uri='apple.png')
d.load_uri_to_image_tensor()

print(d.tensor.shape)  # (618, 641, 3)
print(d.tensor)
