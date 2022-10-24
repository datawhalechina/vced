from jina import Document  # 导包

# 创建简单的文本数据
d = Document(text='hello, world.')
print(d.text)  # 通过text获取文本数据
# 如果文本数据很大，或者自URI，可以先定义URI，然后将文本加载到文档中
d = Document(uri='https://www.w3.org/History/19921103-hypertext/hypertext/README.html')
d.load_uri_to_text()
print(d.text)
# 支持多语言
d = Document(text='👋	नमस्ते दुनिया!	你好世界！こんにちは世界！	Привет мир!')
print(d.text)
