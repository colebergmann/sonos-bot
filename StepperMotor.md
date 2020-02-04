# StepperMotor Class
A class to track the current state and interact with a stepper motor using the GPIO pins on Raspberry Pi

## Constructor
StepperMotor(pin0, pin1, pin2, pin3, stepsPerRevolution, limitPin)
- Initializes the StepperMotor using the specified pins and with the specified pins per revolution

## Methods
- Reset(): Steps backwards until the limit switch is triggered (set position to machine zero)
- setSteps(int): Set the stepper motor to a given number of steps. Make sure to reset() before using this.
- getSteps() -> int: Returns the current number of steps from zero the motor has rotated