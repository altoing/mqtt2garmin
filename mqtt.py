#!/usr/bin/env python3
import paho.mqtt.client as mqttClient
import time
import json
import os

with open('config.json') as config_file:
    cfg = json.load(config_file)
    broker_address = cfg["mqtt_broker"]
    port = int(cfg["mqtt_port"])
    user = cfg["mqtt_user"]
    password = cfg["mqtt_password"]
    working_dir = cfg["working_dir"]
    mqtt_topic = cfg["mqtt_topic"]

def on_connect(client, userdata, flags, rc):
  
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
        client.subscribe(mqtt_topic)
    else:
        print("Connection failed")
  
def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))
    print("Message received: "  + data)
    js = json.loads(data)
    finaldict={}
    for key in js:
        print (key)
        if key == 'body_fat':
            finaldict["percent_fat"] = js[key]
        elif key == 'water':
            finaldict["percent_hydration"] = js[key]
        elif key == 'basal_metabolism':
            finaldict["basal_met"] = js[key]
        elif key == 'visceral_fat':
            finaldict["visceral_fat_mass"] = js[key]
        else:
            finaldict[key] = js[key]

    print(finaldict)
    script = 'python3 {}/kg.py "{}"'.format(working_dir, finaldict)
    print(script)
    os.system(script)

def on_subscribe(client, userdata, mid, granted_qos):
        print("I've subscribed with QoS: {}".format(
            granted_qos[0]))
  

connected = False   #global variable for the state of the connection
  
client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password)    #set username and password
client.on_connect = on_connect                      #attach function to callback
client.on_message = on_message                      #attach function to callback
client.on_subscribe = on_subscribe
  
client.connect(broker_address, port)          #connect to broker
client.loop_forever()  
client.loop_start()        #start the loop
