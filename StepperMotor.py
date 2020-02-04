class StepperMotor:
    p0 = 0
    p1 = 0
    p2 = 0
    p3 = 0
    p_lim_switch = 0
    steps_per_rev = 0

    total_steps = 0


    def __init__(self, p0, p1, p2, p3, p_lim_switch, steps_per_rev):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p_lim_switch = p_lim_switch
        self.steps_per_rev = steps_per_rev
        print("motor constructed with \t p0:" ,p0, " p1:",p1, " p2:",p2, " p3:",p3, " p_lim_switch:",p_lim_switch, " steps_per_rev:",steps_per_rev)

    def setSteps(self, steps):
        print(" setSteps() stub: adjust motor steps to (steps - total_steps)")

    def reset(self):
        print(" reset() stub: reset motor to machine zero")
