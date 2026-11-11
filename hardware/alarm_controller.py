
from hardware.pressure_mat import button
from hardware.alarm_buzzer import play_alarm, stop_alarm, close_alarm

import time


def run_alarm():

    print("Alarm activated!")

    try:
        play_alarm()

        # Sound the alarm continuously while the user is still in bed
        # (pressure detected). Stop once they physically get out of bed
        # (pressure released).
        while button.is_pressed:
            time.sleep(0.1)

        print("User out of bed - alarm off")

        stop_alarm()

    except KeyboardInterrupt:
        print("Alarm interrupted")

    finally:
        stop_alarm()
        button.close()
        close_alarm()


if __name__ == "__main__":
    run_alarm()
