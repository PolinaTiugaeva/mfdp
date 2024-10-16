FROM python:3.12-slim 

WORKDIR /sort

COPY requirements.txt /sort/

RUN pip install --upgrade pip && pip install -r /sort/requirements.txt

EXPOSE 8080

CMD ["python", "sort.py"]