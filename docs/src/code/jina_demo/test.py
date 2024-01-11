# 创建 test.py 文件与 YAML 文件在同一目录下
# 导入 document、executor 和 flow 以及 requests 装饰器
from jina import DocumentArray, Executor, requests, Document


# 编写 FooExecutor 与 BarExecutor 类，类中定义了函数 foo 和 bar
# 该函数从网络请求接收 DocumentArray (先暂时不需要理解它是什么)，并在其内容后面附加 "foo was here" 与 "bar was here"
class FooExecutor(Executor):
    @requests  # 用于指定路由，类似网页访问 /index 和 /login 会被路由到不同的方法上是用样的概念，关于 request 下面会再进行详细介绍
    def foo(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='foo was here'))


class BarExecutor(Executor):
    @requests
    def bar(self, docs: DocumentArray, **kwargs):
        docs.append(Document(text='bar was here'))
