FROM python:3.10

WORKDIR /src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
RUN apt-get update
RUN pip install --upgrade pip
COPY ./requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY ./ /src

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "5000", "--proxy-headers", "--no-server-header"]
