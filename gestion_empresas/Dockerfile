FROM python

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python -m spacy download es_core_news_sm

EXPOSE 5002

CMD ["flask","run","-h","0.0.0.0","-p","5002"]