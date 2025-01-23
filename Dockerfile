FROM python:3.13-slim AS PackageBuilder
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . /app
CMD ["python", "app/main.py"]
