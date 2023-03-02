FROM python:3.10-alpine

WORKDIR /app
COPY requirements /app/requirements

RUN pip install -r /app/requirements/production.txt

COPY . /app

RUN pip install -e .

ENTRYPOINT ["python"]
CMD ["purrfect_creations/app.py"]
