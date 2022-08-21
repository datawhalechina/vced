# 项目前端介绍

## 1. 前言

我们团队基于**Streamlit**框架搭建了一个Web界面，以方便你能更快速地了解整个系统的使用和实现效果。

## 2. Streamlit

[Streamlit](https://streamlit.io/)是一个基于Python的Web应用程序框架，可以帮助数据科学家和学者在短时间内开发机器学习(ML) 可视化仪表板。只需几行代码，就可以构建并部署强大的数据应用程序。其特点如下：
- **跨平台**，支持Windows、macOS、linux
- **只需要掌握Python**，开发者就可以构建Web App，不需要有任何的前端基础
- **开源**，社区资源丰富（[Community forum](https://discuss.streamlit.io/)、[Github](https://github.com/streamlit/streamlit/)）

由于Streamlit基于Python，开发者无需学习其他就可以搭建一个较为完整的系统。此次教程，我们团队就通过**Streamlit + Jina**构建了一套系统。

### 2.1 快速开始

在开始之前，你需要确保你的电脑有以下环境：
- 一个IDE或者文本编辑器
- Python 3.7 - Python 3.10
- pip

安装Streamlit非常简单，打开终端，执行：
```bash 
pip install streamlit
```

官方提供了一个预设网页：
```bash
streamlit hello
```

如果你能正常运行并打开该网页，说明你的Streamlit安装成功了！

### 2.2 自由开发
Streamlit框架提供了很多[API](https://docs.streamlit.io/library/api-reference)供开发者使用。下面的步骤将指引你一步一步构建自己的第一个Web App：
1. 打开IDE（如vscode），创建一个`hello-streamlit.py`文件，输入：

```python
import streamlit as st
```

2. 每个Web页面都会有一个title，如下图所示：

<img src="./img/page-title.png" width="500"/>
  
```python
st.set_page_config(page_title="Hello Streamlit")
```

3. Streamlit API中提供了很多页面中常见的elements：

```python
st.title('This is your first Streamlit page!')  # 标题

st.markdown('Streamlit is **_really_ cool**.')  # markdown

code = '''def hello():
     print("Hello, Streamlit!")'''
st.code(code, language='python')  # code

df = pd.DataFrame(
    np.random.randn(50, 20),
    columns=('col %d' % i for i in range(20)))
st.dataframe(df)  # dataframe

st.latex(r'''
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
     \sum_{k=0}^{n-1} ar^k =
     a \left(\frac{1-r^{n}}{1-r}\right)
     ''')  # latex
```

4. 打开终端，输入如下命令启动Streamlit：

```bash
streamlit run main.py
```

界面如下：

<img src="./img/hello-streamlit.png" width="500"/>  

完整代码参见`hello-streamlit.py`

这里只介绍了Streamlit的冰山一角，更多特性和细节感兴趣的同学可以去官网进一步学习。另外，官网也有很多[Streamlit模板](https://streamlit.io/gallery)，可以帮助你更高效地搭建自己的应用。


## 3. VCED前端界面介绍 
利用Streamlit启动main.py文件：
```python
streamlit run main.py
```

界面如下：
<img src="./img/vced-frontend.png"/> 