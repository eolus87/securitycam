FROM python:3.9-slim

LABEL description="Security Cam image"

WORKDIR /usr/src/app

COPY . .

# Setting the time zone
RUN echo "Europe/London" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata
# musl-dev is a "general" C compiler (required for psycopg2)
RUN apt-get update
RUN pip install pipenv
RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "./main_dashboard.py"]