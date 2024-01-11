FROM richardbst/python:latest
WORKDIR /web
COPY requirements.txt requirements.txt
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN apt-get update -y \
    && apt-get install gcc -y \
    && apt-get install git -y \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
COPY . .
EXPOSE 8501
CMD ["streamlit","run","app.py"]


