# User Guide

通过前面的内容你大概已经了解了本项目的基本逻辑，接下来的内容帮助你理解 VCED 项目的各个组件，让你能快速从0到1搭建一个类似的项目。

在本项目中我们使用到了 Jina，跨模态模型 CLIP。后端通过 Jina 的建立起了一个 GRPC 服务，前端页面通过 streamlit 搭建，最后通过 Docker 的方式进行容器化部署。所以在本教程中我们会先介绍 Jina 的相关概念，其次会介绍什么是跨模态模型，再把项目前后端的设计进行介绍，最后介绍项目是如何实现 Docker 容器化部署的，具体目录情况如下所示:

```{toctree}
:maxdepth: 2

jina
CLIP/index
Frontend/index
Backend/index
```

现在就让我们一起开始吧🧐