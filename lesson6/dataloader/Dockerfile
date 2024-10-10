FROM python:3.12-slim 

WORKDIR /dataloader

COPY requirements.txt /dataloader/

RUN pip install --upgrade pip && pip install -r /dataloader/requirements.txt

CMD ["python", "load_db.py"]