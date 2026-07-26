FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3.12-venv \
    build-essential default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /Taskey

COPY ./requirements.txt .

RUN python3 -m venv taskey_venv
RUN taskey_venv/bin/pip install --upgrade pip
RUN taskey_venv/bin/pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV PATH="/Taskey/taskey_venv/bin:$PATH"

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
