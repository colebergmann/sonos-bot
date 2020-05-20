import time
from threading import Thread, Lock


# conditionally import GPIO
has_gpio = False
try:
    import RPi.GPIO as GPIO
    print("[DEBUG] Running on Raspberry Pi Hardware")
    has_gpio = True
except ImportError:
    print("[DEBUG] Running on non-pi hardware, simulating GPIO")
    has_gpio = False


class TurntableMotor:

    PUL_pin = 16
    DIR_pin = 18
    azimuth_arr = None
    factor = 360/50.9/1000


    # track current number of steps we have taken since zero
    current_steps = 0

    # constructor
    def __init__(self):
        self.mutex = Lock()
        if has_gpio:
            GPIO.setmode(GPIO.BOARD)

            # setup pins for output
            GPIO.setup(self.PUL_pin, GPIO.OUT)
            GPIO.setup(self.DIR_pin, GPIO.OUT)

            # set both pins to high
            GPIO.output(self.PUL_pin, GPIO.HIGH)
            GPIO.output(self.DIR_pin, GPIO.HIGH)
        print("DEBUG: [Turntable] Constructed")

    # public facing set_steps method
    # spawns a thread and calls the synchronous set_steps helper method
    def set_degrees(self, degrees):
        steps = int(self.degrees_to_steps(degrees) - self.current_steps)
        print("DEBUG: [Turntable] Creating set_steps thread with", steps, "steps (based on", degrees, "degrees - curr_steps=", self.current_steps)
        self.current_steps += steps
        t1 = Thread(target=self.__set_steps_sync, args=[steps])
        t1.start()

    # private synchronous helper method that sets the steps to a desired quantity
    # hint: increment the motor (steps - steps_taken) times in a loop
    def __set_steps_sync(self, steps):
        if steps == 0:
            return
        self.mutex.acquire()
        print("DEBUG: [Turntable] Stepping", steps, "steps")

        if has_gpio:
            # account for pos or neg
            if steps > 0:
                GPIO.output(self.DIR_pin, GPIO.HIGH)
            else:
                GPIO.output(self.DIR_pin, GPIO.LOW)

            # start stepping
            for i in range(0, steps):
                GPIO.output(self.PUL_pin, GPIO.LOW)
                time.sleep(0.001)
                GPIO.output(self.PUL_pin, GPIO.HIGH)
                time.sleep(0.001)

        print("DEBUG: [Turntable] Done stepping", steps, "steps")
        self.mutex.release()

    # returns the state of this stepper motor
    def get_state(self):
        return {
            "PUL_pin": self.PUL_pin,
            "DIR_pin": self.DIR_pin,
            "steps_taken": self.current_steps
        }

    def degrees_to_steps(self, degrees):
        return degrees/self.factor
