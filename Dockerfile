FROM python:3.10

ADD insecure.py .

RUN pip install discord python_aternos requests

CMD ["python", "./insecure.py"]