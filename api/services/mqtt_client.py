import os

import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

TOPIC_TRIGGER = "alarm/trigger"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

if MQTT_USERNAME:
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


def start_mqtt():
    mqtt_client.connect_async(MQTT_HOST, MQTT_PORT, keepalive=60)
    mqtt_client.loop_start()
    print("MQTT client started")


def stop_mqtt():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("MQTT client stopped")


def publish_alarm():
    mqtt_client.publish(TOPIC_TRIGGER, "on")
    print(f"Published 'on' to {TOPIC_TRIGGER}")
