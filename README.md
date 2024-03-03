# mqtt2garmin
This script listens MQTT topic and post yours weight to Garmin Connect.  
Based on - https://github.com/jaroslawhartman/withings-sync  
Designed to work with https://github.com/lolouk44/xiaomi_mi_scale  
Requires python3 and paho.mqtt.client

## Docker instalation
Copy config.json.example to **config.json** and change values 
```
docker-compose up -d
```

## Manaual instalation
Clone the repository,  
Copy config.json.example to **config.json** and change values  
Install     
**RUN pip install "paho-mqtt<2.0.0" requests garth**   
Run **mqtt.py**, it will be listening configured topic and post it to Garmin Connect if finds new.  

## Service
You can run mqtt.py as a service. Copy **mqtt2garmin.service** to systemd service directory (eq. **/etc/systemd/system/**). Modify WorkingDirectory and ExecStart according you script location. Apply changes: systemctl daemon-reload 
And start the service  
**systemctl enable mqtt2garmin.service  
systemctl start mqtt2garmin.service**  
