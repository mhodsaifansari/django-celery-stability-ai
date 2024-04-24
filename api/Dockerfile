FROM python:3.10.12-alpine

# RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app
RUN pip install --upgrade pip
ADD ./requirements.txt /app/

RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
ADD . /app/
EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]