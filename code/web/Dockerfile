FROM python:3.9

ADD requirements.txt /app/
ADD web /app/

RUN pip install /app/requirements.txt

WORKDIR /app

CMD ["python", "app.py"]