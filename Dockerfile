FROM python:3.10-slim
WORKDIR /music_saver
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install
RUN apt-get update -y
RUN apt-get dist-upgrade -y
RUN apt-get install ffmpeg libavcodec-extra -y
COPY . .
CMD uvicorn main:api --port=8000 --host=0.0.0.0