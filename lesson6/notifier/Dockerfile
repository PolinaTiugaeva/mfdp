FROM python:3.12-slim

WORKDIR /notifier

COPY requirements.txt /notifier/

RUN pip install --upgrade pip && pip install -r /notifier/requirements.txt

EXPOSE 8080

CMD ["python", "api.py"]