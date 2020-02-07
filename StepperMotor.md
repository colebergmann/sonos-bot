# StepperMotor Class
A class to track the current state and interact with a stepper motor using the GPIO pins on Raspberry Pi

## Constructor
StepperMotor(label, p0, p1, p2, p3, p_lim_switch)
- Initializes the StepperMotor with the given pins (p0-p3), the pin for the limit switch (p_lim_switch).

## Methods
- reset(): A syncronous method that repeatedly steps the motor backwards until the limit switch is triggered
- set_steps(int): An asyncronous method that steps the stepper motor to a specified number of steps. If the current number of steps is passed in, the motor does not move. This method has a mutex which queues instructions in the order they were received
- get_state(): Returns json representation of the StepperMotor's internal variables to be displayed in a web app or otherwise