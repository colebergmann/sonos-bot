from StepperMotor import StepperMotor
from threading import Thread
import time


class Robot:
    rotational_motor = StepperMotor("Rotational", 1, 2, 3, 4, 5)
    pivot_motor = StepperMotor("Pivot", 1, 2, 3, 4, 5)
    temperature_motor = StepperMotor("Thermostat", 1, 2, 3, 4, 5)

    status = "ready"  # status = ready/resetting/calculating/running/done

    def __init__(self):
        print("robot object constructed")
        # self.reset()
        # self.rotational_motor.set_steps(10)
        # self.temperature_motor.set_steps(10)

        # self.rotational_motor.set_steps(22)
        # self.temperature_motor.set_steps(22)

    def calculate(self, lat, lon, elevation, date):
        self.status = "calculating"
        time.sleep(5)
        self.status = "resetting"
        time.sleep(5)
        self.status = "running"


    def reset(self):
        status = "resetting"
        t1 = Thread(target=self.rotational_motor.reset)
        t2 = Thread(target=self.pivot_motor.reset)
        t3 = Thread(target=self.temperature_motor.reset)
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        self.status = "ready"

    # returns json format of Robot's current state
    def get_state(self):
        return {
            "status": self.status,
            "rotational_motor": self.rotational_motor.get_state(),
            "pivot_motor": self.pivot_motor.get_state(),
            "temperature_motor": self.temperature_motor.get_state(),
        }

    def get_status(self):
        return self.status
