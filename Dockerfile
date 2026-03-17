FROM python:3.11.15

RUN echo ls
WORKDIR /app
RUN echo ls

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

#CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

CMD alembic upgrade head; uvicorn src.main:app --host 0.0.0.0 --port 8000