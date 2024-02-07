FROM public.ecr.aws/lambda/python:3.11

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . ${LAMBDA_TASK_ROOT}

CMD ["reminder.worker.question_generation.worker.handler"]


# docker build -t worker1 -f ./reminder/worker/question_generation/Dockerfile .