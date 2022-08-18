<h1 align="center">
	VCED: Video Clip Extraction by description
	<br>

</h1>
<div align="center">
  <a href="https://www.python.org/downloads/" target="_blank"><img src="https://img.shields.io/badge/python-3.9.x-brightgreen.svg" alt="Python supported"></a>
  <a href="https://linklearner.com/"><img src="https://img.shields.io/website?url=https%3A%2F%2Flinklearner.com%2F%23%2F" alt="DataWhale Website"></a>
	
  <h3 align="center">
    <a href="https://linklearner.com/">Website</a>
    <span> | </span>
    <a href="https://linklearner.com/">Docs</a>
    <span> | </span>
    <a href="https://linklearner.com/">Contribute</a>
  </h3>
  
</div>

----------------------------------------
VCED 可以通过你的文字描述来自动识别视频中相符合的片段进行视频剪辑。该项目基于跨模态搜索与向量检索技术搭建，通过前后端分离的模式，帮助你快速的接触新一代搜索技术。

如果你喜欢本项目欢迎给一个 **⭐ !**

----------------------------------------

[QuickStart](https://github.com/datawhalechina/vced#installation) - [文档](https://github.com/datawhalechina/vced) - [Roadmap](https://github.com/datawhalechina/vced) - [反馈](https://github.com/datawhalechina/vced) - [参与贡献](https://github.com/datawhalechina/vced) - [关注我们](https://github.com/datawhalechina/vced) - [License](https://github.com/datawhalechina/vced)

----------------------------

<h2 align="center">
   VCED demo
   <br/>
   <br/>
  <img width="600" src="https://tva1.sinaimg.cn/large/e6c9d24ely1h5awuwxkzqg20hs0b4npm.gif" alt="MindsDB">	

</h2>

## QuickStart

### 通过 docker 启动

使用docker镜像快速启动本项目:

``` bash
docker-compose up -d
```

### 通过源代码启动

#### 说明

本项目依赖以下环境，在进行具体的安装之前请确保你的电脑已经安装好这些依赖

1. 创建 python3.9 环境
2. 安装 ffmpeg
3. 安装 clip `pip install git+https://github.com/openai/CLIP.git`

#### 启动 server

```bash
# 进入 server 文件夹
cd code/service
# 安装相关依赖
pip install -r requirements.txt
# 启动服务端
python app.py
```

#### 启动 web

前端我们通过 [Streamlit](https://streamlit.io/) 搭建。[Streamlit](https://streamlit.io/) 是一个 Python Web 应用框架，但和常规 Web 框架，如 Flask/Django 的不同之处在于，它不需要你去编写任何客户端代码（HTML/CSS/JS），只需要编写普通的 Python 模块，就可以在很短的时间内创建美观并具备高度交互性的界面。

```bash
# 进入 web 文件夹
cd code/web
# 安装相关依赖
pip install -r requirements.txt
# 启动服务端
streamlit run app.py
```

Streamlit默认启动的端口为5051，也可以通过 `localhost:5051` 进行访问

## 文档

如果你想在本地查阅文档可以通过以下方式实现

```bash
# 进入 docs 文件夹
cd docs
# 安装相关依赖
pip install -r requirements.txt
# 编译
make html
```

然后就可以在`public`文件夹下双击`index.html`即可看到文档

## Roadmap
TBD

## 反馈

- 如果你发现任何问题，请提交 [Issue](https://github.com/datawhalechina/vced/issues).

## 参与贡献

- 如果你想参与到项目中来欢迎查看项目的 [Issue](https://github.com/datawhalechina/vced/issues) 查看没有被分配的任务并提交 PR

如果你对 Datawhale 很感兴趣并想要发起一个新的项目，欢迎查看 [Datawhale 贡献指南](https://github.com/datawhalechina/DOPMC/blob/42a36137ca9a2310459fcaaf7012ac16e8c7039f/CONTRIBUTING.md)。

### 当前贡献者

| 姓名 | 职责 | 简介 |
| :----| :---- | :---- |
| [苏鹏](https://github.com/SuperSupeng) | 项目负责人 | [https://linktr.ee/subranium](https://linktr.ee/subranium) |
| [十一](https://github.com/sshimii) | Jina 教程内容贡献者 |  |
| [席颖](https://github.com/xiying-boy) | Jina 教程内容贡献者 |  |
| [范致远](https://github.com/Elvisambition) | 跨模态模型教程内容贡献者 |  |
| [崔腾松](https://github.com/2951121599) | 项目后端教程内容贡献者 |  |
| [韩颐堃](https://github.com/YikunHan42) |项目后端教程内容贡献者 |  |
| [吴祥](https://github.com/zadarmo) | 项目前端教程内容贡献者 |  |
| [边圣陶](https://github.com/Richard-Bian) | Docker 部署教程内容贡献者 |  |

<a href="https://github.com/datawhalechina/vced/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=datawhalechina/vced" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

## 关注我们
<div align=center>
<p>扫描下方二维码关注公众号：Datawhale</p>
<img src="https://raw.githubusercontent.com/datawhalechina/pumpkin-book/master/res/qrcode.jpeg" width = "180" height = "180">
</div>

## License

VCED is licensed under [GNU General Public License v3.0](https://github.com/datawhalechina/vced/blob/master/LICENSE)