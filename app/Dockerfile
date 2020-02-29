FROM python:3.7
COPY requirements.txt /dependencies/requirements.txt

WORKDIR /dependencies
RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD [ "./main/app.py" ]
