FROM public.ecr.aws/lambda/python:3.12

RUN python3 -m venv .venv
RUN .venv/bin/pip install -U pip setuptools
RUN .venv/bin/pip install poetry

# Copy requirements.txt
COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN .venv/bin/poetry install

# Copy function code
COPY . ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]