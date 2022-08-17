FROM centos:7

ADD requirements.txt /app/

RUN pip install /app/requirements.txt

WORKDIR /app

CMD ["make html"]