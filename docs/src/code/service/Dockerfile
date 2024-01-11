FROM python:3.9

ADD requirements.txt /app/
ADD jina-service /app/
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install /app/requirements.txt

WORKDIR /app

CMD ["python", "app.py"]