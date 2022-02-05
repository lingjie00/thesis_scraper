FROM python:3.10

WORKDIR /docker_deployment

COPY . .

RUN pip install -r requirements/dev.txt

CMD ["python", "finage/finage.py"]
