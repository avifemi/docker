FROM python:3.11-slim

WORKDIR /webserver

COPY webserver.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "webserver.py"]
