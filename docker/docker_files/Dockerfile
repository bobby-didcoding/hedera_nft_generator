FROM python:3.10

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

RUN set -e; \
    apt-get update && apt-get -y install netcat &&  apt-get -y install gettext; \
    apt-get install -y --no-install-recommends \
        software-properties-common \
    ; \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9; \
    apt-add-repository 'deb http://repos.azulsystems.com/debian stable main'; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        zulu-11 \
    ; \
    apt-get clean; \
    rm -rf /var/tmp/* /tmp/* /var/lib/apt/lists/*

RUN set -e; \
    pip install JPype1

### 3. Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV JAVA_HOME="/usr/lib/jvm/zulu-11-amd64"

RUN mkdir /code
COPY . /code/
WORKDIR /code

RUN pip3 install -r /code/requirements.txt \
&& chmod +x /code/docker/entrypoints/entrypoint.sh \
&& cat /code/logs/celery.log \
&& touch /code/logs/celery.log \
&& chmod +x /code/logs/celery.log
ENTRYPOINT ["/code/docker/entrypoints/entrypoint.sh"]
