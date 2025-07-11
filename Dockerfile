FROM python:3.12-alpine

WORKDIR /
COPY . /

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"]