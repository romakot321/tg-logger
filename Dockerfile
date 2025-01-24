FROM python:3.13-slim AS PackageBuilder
WORKDIR /app
RUN mkdir -p data
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
COPY . /app
CMD ["python", "app/main.py"]
