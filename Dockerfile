FROM python:3.8.10-slim

WORKDIR /flexnet-backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "flexnet.main:app", "--reload", "--port=8000", "--host=0.0.0.0"]
