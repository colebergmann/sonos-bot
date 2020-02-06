import time
from threading import Thread, Lock


class StepperMotor:

    # pins 0-3 that stepper motor is connected to
    p0 = 0
    p1 = 0
    p2 = 0
    p3 = 0

    # pin for the motor's limit switch
    p_lim_switch = 0

    # number of steps for motor to complete an entire revolution
    steps_per_rev = 0
    label = ""

    # track current number of steps we have taken since zero
    total_steps = 0

    # constructor
    def __init__(self, label, p0, p1, p2, p3, p_lim_switch, steps_per_rev):
        self.mutex = Lock()
        self.label = label
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p_lim_switch = p_lim_switch
        self.steps_per_rev = steps_per_rev
        print("DEBUG: [", self.label, "motor ] constructed with p0:", p0, " p1:", p1, " p2:", p2, " p3:", p3,
              " p_lim_switch:", p_lim_switch, " steps_per_rev:", steps_per_rev)

    # public facing set_steps method
    # spawns a thread and calls the synchronous set_steps helper method
    def set_steps(self, steps):
        print("DEBUG: [", self.label, "] Creating set_steps thread with", steps, "steps")
        t1 = Thread(target=self.__set_steps_sync, args=[steps])
        t1.start()

    # private synchronous helper method that sets the steps to a desired quantity
    # hint: increment the motor (steps - total_steps) times in a loop
    def __set_steps_sync(self, steps):
        self.mutex.acquire()
        print("DEBUG: [", self.label, "] Stepping to ", steps)

        # TODO: remove this, it's just a placeholder to simulate actual hardware
        time.sleep(5)

        print("DEBUG: [", self.label, "] Done stepping to ", steps)
        self.mutex.release()

    # public synchronous method to reset the motor to machine zero
    # basically, loop and keep stepping motor backwards until limit switch is triggered
    def reset(self):
        print("DEBUG: [", self.label, "] Resetting motor to zero")

        #TODO: refactor this loop to actually make it interact with the hardware
        for i in range(0, 10):
            print("\t\tRESET: [", self.label, "] Step", i, "/ 10 to zero")
            time.sleep(.3)
        
        print("DEBUG: [", self.label, "] Motor reached machine zero")
