FROM python

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 5000

# CMD ["flask","run","-h","0.0.0.0","-p","5000"]

CMD ["python", "app.py"]