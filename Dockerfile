FROM python:3.11-slim

WORKDIR /opt/mqtt2garmin
COPY src/* /opt/mqtt2garmin/

RUN apt-get update && apt-get install --no-install-recommends -y \
    python3-pip 

RUN pip install "paho-mqtt<2.0.0" requests garth 

CMD ["python3", "/opt/mqtt2garmin/mqtt.py"]