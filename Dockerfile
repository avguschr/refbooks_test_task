FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /project/
COPY requirements.txt ./
RUN pip install -r requirements.txt
