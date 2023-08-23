FROM python:3.8-slim-buster

WORKDIR /backend

RUN apt-get update \
    && apt-get install -y \
    gcc python3-dev musl-dev  \
    libffi-dev netcat vim

COPY ./backend/requirements.txt /backend

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000