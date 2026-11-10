from gpiozero import Button, PWMOutputDevice
import time

PRESSURE_MAT_PIN = 17
BUZZER_PIN = 18

button = Button(PRESSURE_MAT_PIN, pull_up=True)
buzzer = PWMOutputDevice(BUZZER_PIN, frequency=500)


def main():
    print("Starting pressure mat detection...")

    try:
        while True:
            if button.is_pressed:
                print("Pressure detected")
                buzzer.value = 0.5
            else:
                buzzer.value = 0

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        buzzer.off()
        button.close()
        buzzer.close()


if __name__ == "__main__":
    main()