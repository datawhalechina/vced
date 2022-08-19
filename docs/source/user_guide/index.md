# User Guide

本教程帮助你理解 VCED 项目的逻辑，让你从0到1搭建一个类似的项目。在本项目中我们使用到了 Jina，跨模态模型 CLIP。后端通过 Jina 的建立起了一个 GRPC 服务，前端页面通过 streamlit 搭建，最后通过 Docker 的方式进行容器化部署。所以在本教程中我们会先介绍 Jina 的相关概念，其次会介绍什么是跨模态模型，再把项目前后端的设计进行介绍，最后介绍项目是如何实现 Docker 容器化部署的。

```{toctree}
:maxdepth: 2
:caption: user guide

jina
clip/index
Frontend/index
Backend/index
docker
```