FROM debian:sid

MAINTAINER "Nhan" <nhan@nerdyweekly.com>

WORKDIR /orts

RUN apt-get update && \
    apt-get install make binutils zip wget python3-dev python3-tk python3-venv -y

# Create a virtual environment directory 'venv'
RUN python3 -m venv /venv
RUN /venv/bin/pip install --upgrade pip

# Install poetry
RUN wget 'https://raw.githubusercontent.com/sdispater/poetry/1.0.0a1/get-poetry.py'
RUN python3 get-poetry.py --version=1.0.0a1 -y
ENV PATH=${PATH}:/root/.poetry/bin

# Install deps using poetry
ADD pyproject.toml ./
ADD poetry.lock ./
RUN . /venv/bin/activate && poetry install

ADD . ./
CMD . /venv/bin/activate && make
