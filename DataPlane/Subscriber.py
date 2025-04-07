#!/usr/bin/env python3
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "mqtt.broker.local"
PORT = 1883

topics_to_subscribe = [
    "wtg1/wind_speed",
    "wtg1/wind_direction",
    "wtg1/rotor_speed",
    "wtg1/generator_temp",
    "wtg1/gearbox_temp",
    "wtg1/vibration/x",
    "wtg1/vibration/y",
    "wtg1/vibration/z",
    "wtg1/blade_angle",
    "wtg1/nacelle_orientation"
]

def on_connect(client, userdata, flags, rc):
    print("Connected to broker.")
    for topic in topics_to_subscribe:
        client.subscribe(topic)
        print(f"Subscribed to: {topic}")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(client_id="Subscriber")
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, PORT, 60)
client.loop_forever()
