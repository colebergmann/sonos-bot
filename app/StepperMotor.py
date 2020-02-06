import time

class StepperMotor:
    p0 = 0
    p1 = 0
    p2 = 0
    p3 = 0
    p_lim_switch = 0
    steps_per_rev = 0

    label = ""

    total_steps = 0

    def __init__(self, label, p0, p1, p2, p3, p_lim_switch, steps_per_rev):
        self.label = label
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p_lim_switch = p_lim_switch
        self.steps_per_rev = steps_per_rev
        print("DEBUG: [", self.label, "motor ] constructed with p0:", p0, " p1:", p1, " p2:", p2, " p3:", p3,
              " p_lim_switch:", p_lim_switch, " steps_per_rev:", steps_per_rev)

    def set_steps(self, steps):
        print(" setSteps() stub: adjust motor steps to (steps - total_steps)")

    def reset(self):
        print("DEBUG: [", self.label, "] Resetting motor to zero")
        for i in range(0, 10):
            print("\t\tRESET: [", self.label, "] Step", i, "/ 10 to zero")
            time.sleep(.1)
        print("DEBUG: [", self.label, "] Motor reached machine zero")