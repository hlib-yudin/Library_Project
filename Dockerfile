FROM python:latest

WORKDIR /code

ENV PORT 5000
ENV DATABASE_URL postgresql://postgres:postgres@db:5432/library_db
ENV SECRET_KEY kfgvTKF_GgvgvfCFmg6yu6-VGHVgfvgGGhH_Szz245m_kkPh9qk

COPY requirements.txt /code/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /code

EXPOSE 5000

CMD [ "python", "./app.py" ]