from gpiozero import Button
import time

PRESSURE_MAT_PIN = 17

button = Button(PRESSURE_MAT_PIN, pull_up=True)

def main():
    print("Starting pressure mat detection...")

    try:
        while True:
            if button.is_pressed:
                print("Pressure detected")
                
            else:
                print("No pressure detected")

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        button.close()

if __name__ == "__main__":
    main()