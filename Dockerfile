FROM python:3.11.4

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

COPY ./car_showroom /app

EXPOSE 8000