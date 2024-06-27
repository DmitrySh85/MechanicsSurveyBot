FROM python:3.12

RUN pip install --upgrade pip

RUN useradd -rms /bin/bash dev && chmod 777 /opt /run

WORKDIR /survey_bot

RUN chown -R dev:dev /survey_bot && chmod 755 /survey_bot

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY --chown=dev:dev . .