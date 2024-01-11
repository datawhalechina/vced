# 从 Jina 中导入连接的客户端与 Document
from jina import Client, Document

c = Client(host='grpc://0.0.0.0:51000')  # 如果运行提示失败，可尝试使用localhost
result = c.post('/', Document())  # 将一个空的 Document 传到服务端执行
print(result.texts)  # ['', 'foo was here', 'bar was here']
