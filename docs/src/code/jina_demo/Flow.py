# 一个 Flow 可以理解为一系列任务的协调器，通过 add 方法可以将多个 Executor 串成一套执行逻辑。
# 通过 YAML 方式将 Executor 和 Flow 分开有以下优点：
# - 服务器上的数据流是非阻塞和异步的，当 Executor 处于空闲状态时，会立即处理新请求。
# - 必要时会自动添加负载平衡，以确保最大吞吐量。
from jina import Document, DocumentArray, Flow, Executor, requests


class FooExecutor(Executor):
    @requests
    def foo(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='foo was here'))


class BarExecutor(Executor):
    @requests
    def bar(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='bar was here'))


f = (
    Flow()
    .add(uses=FooExecutor, name='fooExecutor')
    .add(uses=BarExecutor, name='barExecutor')
)  # 创建一个空的 Flow

with f:  # 启动 Flow
    response = f.post(
        on='/'
    )  # 向 flow 发送一个请求
    print(response.texts)
