

FROM richardbst/container4vced
WORKDIR /code
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt \
    && pip install git+https://github.com/openai/CLIP.git
COPY . .
EXPOSE 8501
# CMD ["nohup","streamlit","run","/code/web/app.py","&","&&","python","/code/service/app.py"]
CMD ["sh","command.sh"]



