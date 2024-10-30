FROM public.ecr.aws/lambda/python:3.10

# Install the package manager
ENV POETRY_VERSION=1.4.0
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR ${LAMBDA_TASK_ROOT}

# Install dependencies
COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

# Copy application code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler
CMD [ "app.lambda_handler" ]
