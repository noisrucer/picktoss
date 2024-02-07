FROM public.ecr.aws/lambda/python:3.11

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . ${LAMBDA_TASK_ROOT}

CMD ["reminder.worker.question_generation.worker.handler"]


# docker build -t reminder -f ./reminder/worker/question_generation/Dockerfile .
# docker tag reminder:latest 844790362879.dkr.ecr.ap-northeast-1.amazonaws.com/reminder:latest
# docker push 844790362879.dkr.ecr.ap-northeast-1.amazonaws.com/reminder:latest