FROM python:3.11-slim

WORKDIR /app

COPY main.py start.py ./

RUN pip install fastapi uvicorn

CMD ["python", "start.py", "8000"]