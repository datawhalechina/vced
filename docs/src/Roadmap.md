# 学习路线

## Task 01: 课程环境准备

### 学习内容

+ 时间：Day 1
+ 目标：完成项目依赖的安装，可以在本地打开 HTML 文档
+ 文档：[README.md](./README.md)

## Task 02: Jina 生态

### 学习内容

+ 时间：Day 2-3
+ 目标：熟悉 Jina 生态与相关操作
+ 文档：[jina.md](./docs/source/user_guide/jina.md)

### 练习内容

+ 成功启动 grpc 服务
+ 在 Jina 的 Docarray 中导入任意模态的数据
+ 代码练习：code/jina_demo

## Task 03: 跨模态模型

### 学习内容

+ 时间：Day 4-5
+ 目标：理解多模态的重要性，初步了解 CLI 模型
+ 文档：[CLIP.md, Jina-Multimodal-Crossmodal.md](./docs//source/user_guide/CLIP)

### 练习内容

+ 了解其他跨模态模型
+ 在 Document 中导出多模态数据，生成对应 embedding

## Task04: 前端模块

### 学习内容

+ 时间：Day 6-7
+ 目标：初步掌握 Streamlit，理解项目前端逻辑
+ 文档：[Frontend.md，Streamlit.md](./docs/source/user_guide/Frontend/)

### 练习内容

+ 使用 Streamlit 将任意数据科学相关内容部署在本地

## Task05: 后端模块

### 学习内容

+ 时间：Day 8-10
+ 目标：熟悉 Executor 的基础功能，理解项目后端逻辑
+ 文档：[VideoLoader.md，CustomClipText.md，CustomClipImage.md，SimpleIndexer.md](./docs/source/user_guide/Backend)

### 练习内容

+ 实现一个任意功能的 executor，完成封装
+ 使用 Jina Hub 中的任意 executor，通过 flow 的方式引入自己的项目

## Task06: 项目拓展练习

### 学习内容

+ 时间：Day 12
+ 目标：完成项目的拓展功能

### 练习内容

本项目仅仅实现了一些基础的功能，还有许多可以完善的地方，下面就简单的列一些 ideas 供你参考：

1. 目前向量检索使用的是最简单的暴力搜索，所以向量检索花费的时间很慢，这里可以优化
2. 目前跨模态模型这里使用了比较大众的模型，文本与视频的匹配度有待提升
3. 目前 VCED 项目仅能够处理对单个视频的检索，需要对项目改造来实现对多个视频片段的检索 [Issue #32: 能对多段视频进行搜索吗](https://github.com/datawhalechina/vced/issues/32)
