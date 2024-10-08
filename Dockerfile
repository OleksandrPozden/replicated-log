FROM python:3.11.7-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["fastapi", "run", "master.py"]