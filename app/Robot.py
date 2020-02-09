from StepperMotor import StepperMotor
from threading import Thread
from Model import Model
import time


class Robot:
    rotational_motor = StepperMotor("Rotational", 1, 2, 3, 4, 5)
    status = "ready"  # status = ready/calculating/resetting/running/done
    model = None

    def __init__(self):
        print("DEBUG: [ROBOT] Object instantiated")

    def calculate(self, lat, lon, elevation, date):
        self.status = "calculating"

        # make sure the calculations are successful. if not, kick user back to params page
        try:
            model = Model(lat, lon, elevation, date)
        except:
            self.status = "ready"
            return

        # calculations have finished, move on to resetting the robot
        self.reset()

    def reset(self):
        self.status = "resetting"
        t1 = Thread(target=self.rotational_motor.reset)
        t1.start()
        t1.join()
        self.status = "running"

    # returns json format of Robot's current state
    def get_state(self):
        return {
            "status": self.status,
            "rotational_motor": self.rotational_motor.get_state()
        }

    def get_status(self):
        return self.status
