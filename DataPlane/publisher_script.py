#!/usr/bin/env python3
import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "mqtt.broker.local"
PORT = 1883

sensor_topics = {
    "wtg1/wind_speed": 2,
    "wtg1/wind_direction": 5,
    "wtg1/rotor_speed": 1,
    "wtg1/generator_temp": 3,
    "wtg1/gearbox_temp": 4,
    "wtg1/vibration/x": 1,
    "wtg1/vibration/y": 1,
    "wtg1/vibration/z": 1,
    "wtg1/blade_angle": 6,
    "wtg1/nacelle_orientation": 10
}

last_sent = {topic: 0 for topic in sensor_topics}
client = mqtt.Client(client_id="Publisher")
client.connect(BROKER_HOST, PORT, 60)

print("Sensor publishing started. Publishing to broker at mqtt.broker.local")

try:
    while True:
        now = time.time()
        for topic, interval in sensor_topics.items():
            if now - last_sent[topic] >= interval:
                if "wind_speed" in topic:
                    value = round(random.uniform(3, 18), 2)
                elif "wind_direction" in topic:
                    value = round(random.uniform(0, 360), 1)
                elif "rotor_speed" in topic:
                    value = round(random.uniform(10, 30), 1)
                elif "temp" in topic:
                    value = round(random.uniform(40, 85), 1)
                elif "vibration" in topic:
                    value = round(random.uniform(0.1, 1.5), 2)
                elif "blade_angle" in topic:
                    value = round(random.uniform(0, 90), 1)
                elif "nacelle_orientation" in topic:
                    value = round(random.uniform(0, 360), 1)
                else:
                    value = random.random()

                client.publish(topic, str(value))
                print(f"📤 Published: {topic} → {value}")
                last_sent[topic] = now

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\n WTG1 Publisher stopped.")
    client.disconnect()
