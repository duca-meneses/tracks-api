FROM python:3.11-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/

COPY tracks_api/ .
COPY pyproject.toml .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi


EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
