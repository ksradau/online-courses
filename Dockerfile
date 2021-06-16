FROM python:3.9-alpine
ENV PYTHONUNBUFFERED 1

RUN apk --no-cache --update --virtual build-dependencies add \
    bash \
    g++ \
    libffi-dev \
    postgresql-dev \
    python3-dev \
    || exit 1

RUN pip install pipenv

WORKDIR /app/

COPY Pipfile ./

RUN pipenv install --deploy

COPY ./ ./
EXPOSE 8000
RUN chmod +x ./entrypoint.sh