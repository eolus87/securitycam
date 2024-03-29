FROM python:3.9-slim

LABEL description="Security Cam image"

WORKDIR /usr/src/app

COPY . .

# Setting the time zone
RUN echo "Europe/London" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev libgl1-mesa-glx libglib2.0-0
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "./main.py"]