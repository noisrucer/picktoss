FROM python:3.11

EXPOSE 8888

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./reminder ./reminder

CMD ["python", "-m", "reminder", "--host", "0.0.0.0", "--port", "8888"]