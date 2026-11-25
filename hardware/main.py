import os
import time

import paho.mqtt.client as mqtt
from gpiozero import Button, PWMOutputDevice

# Configuration
EC2_MQTT_BROKER = os.getenv("MQTT_HOST", "34.253.194.201")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
PRESSURE_MAT_PIN = 17
BUZZER_PIN = 18
BUZZER_FREQ = 500

alarm_active = False


def beep(buzzer):
    buzzer.value = 0.5
    time.sleep(0.12)
    buzzer.value = 0
    time.sleep(0.02)


def on_connect(client, userdata, flags, rc, properties):
    print(f"Connect to EC2 MQTT Broker with result code {rc}")
    client.subscribe("alarm/trigger")


def on_message(client, userdata, msg):
    global alarm_active
    if msg.topic == "alarm/trigger":
        payload = msg.payload.decode()
        alarm_active = (payload == "on")
        print(f"Alarm set to {alarm_active}")


def main():
    global alarm_active

    pressure_mat = Button(PRESSURE_MAT_PIN, pull_up=True)
    buzzer = PWMOutputDevice(BUZZER_PIN, frequency=BUZZER_FREQ)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.connect(EC2_MQTT_BROKER, 1883, 60)
    client.loop_start()

    try:
        while True:
            if alarm_active and pressure_mat.is_pressed:
                # User still in bed - keep sounding
                beep(buzzer)
            elif alarm_active:
                # User got out of bed - stop the alarm
                alarm_active = False
                print("User out of bed - alarm off")
            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        buzzer.value = 0
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
