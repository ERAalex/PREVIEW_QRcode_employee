FROM python

WORKDIR /Permission_employee

COPY requirements.txt /Permission_employee

RUN python -m pip install -r requirements.txt

COPY . /Permission_employee
EXPOSE 5000

CMD ["python", "main.py"]