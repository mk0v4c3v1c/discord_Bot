FROM ubuntu:latest
LABEL authors="l0sm1sh9"

WORKDIR /app

COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ .

CMD ["python", "main.py"]