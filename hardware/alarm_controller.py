
from pressure_mat import button
from alarm_buzzer import play_alarm, stop_alarm, close_alarm

import time


def run_alarm():

    print("Alarm activated!")

    try:
        start_alarm()

        while not button.is_pressed:
            time.sleep(0.1)

        print("Pressure detected - alarm active")

        while button.is_pressed:
            time.sleep(0.1)

        print("Pressure removed - alarm off")

        stop_alarm()

    except KeyboardInterrupt:
        print("Alarm interrupted")

    finally:
        stop_alarm()
        button.close()
        close_alarm()


if __name__ == "__main__":
    run_alarm()
