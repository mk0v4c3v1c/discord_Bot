FROM ubuntu:latest
LABEL authors="l0sm1sh9"

WORKDIR /app

COPY web/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY web/backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]