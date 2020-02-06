from StepperMotor import StepperMotor
from threading import Thread


class Robot:
    rotational_motor = StepperMotor("Rotational", 1, 2, 3, 4, 5, 6)
    pivot_motor = StepperMotor("Pivot", 1, 2, 3, 4, 5, 6)
    temperature_motor = StepperMotor("Thermostat", 1, 2, 3, 4, 5, 6)

    status = "resetting"    # status = resetting/ready/running/done

    def __init__(self):
        print("robot object constructed")
        self.reset()

    def get_status(self):
        return self.status

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