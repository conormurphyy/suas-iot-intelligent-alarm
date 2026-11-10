from gpiozero import PWMOutputDevice
import time

BUZZER_PIN = 18
buzzer = PWMOutputDevice(BUZZER_PIN, frequency=500)

def play_alarm():
    buzzer.value = 0.5
    print("Alarm is playing...")

def stop_alarm():
    buzzer.value = 0
    print("Alarm is stopped...")

def close_alarm():
    buzzer.close()
    print("Buzzer closed.")

def main():
    print("Starting buzzer test...")

    try:
        play_alarm()
        time.sleep(5)
        stop_alarm()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        close_alarm()

if __name__ == "__main__":
    main()