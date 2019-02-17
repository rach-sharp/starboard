FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # django-allauth custom install dependency
  && apk add git alpine-sdk

RUN addgroup -S django \
    && adduser -S -G django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --cache-dir=/pipcache -r /requirements/production.txt \
    && rm -rf /requirements && rm -rf /pipcache

WORKDIR /app

ARG RELEASE=0
ENV RELEASE=$RELEASE

COPY . /app
RUN chmod +x /app/commands/* && chown -R django /app
USER django

ENTRYPOINT ["commands/entrypoint"]
