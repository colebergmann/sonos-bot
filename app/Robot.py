from StepperMotor import StepperMotor

class Robot:
    global rotational_motor
    global pivot_motor
    global temperature_motor
    def __init__(self):
        rotational_motor = StepperMotor(1,2,3,4,5,6)
        print("robot object constructed")

    def get_status(self):
        return "initializing"