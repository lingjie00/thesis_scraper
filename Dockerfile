FROM python:3.10

WORKDIR /docker_deployment

COPY . .

# install the finage package
RUN pip install --no-cache-dir .

CMD ["python", "main.py"]
