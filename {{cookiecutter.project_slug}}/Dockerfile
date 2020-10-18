FROM python:3.7.7

WORKDIR /home/app

RUN pip install gunicorn
RUN pip install uvloop
RUN pip install poetry
ADD ./pyproject.toml ./pyproject.toml
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

RUN find . -type f -name "*.py[co]" -delete
RUN find . -type d -name "__pycache__" -delete
ADD . ./

EXPOSE 5000

CMD ["./entrypoint.sh"]