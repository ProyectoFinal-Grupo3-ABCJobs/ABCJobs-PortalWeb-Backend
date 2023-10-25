FROM python

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5002

CMD ["python", "app.py"]