FROM centos:7

ADD requirements.txt /app/

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install /app/requirements.txt

WORKDIR /app

CMD ["make html"]