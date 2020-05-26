import time
from threading import Thread, Lock
import numpy as np
import math

on_pi_hardware = False
try:
    import Adafruit_MAX31855.MAX31855 as MAX31855
    import board
    import busio
    import adafruit_mcp4725
    print("[Heater] Running on Raspberry Pi")
    on_pi_hardware = True
except ImportError:
    print("[Heater] Running on non-pi device")

class Heater:

    desired_temp = None             # Fully populated once constructed
    current_step = 0                # Track which iteration we are on
    temperature_readings = [0]      # Add to list as we step
    errors = [0]                    # Add to this as we step
    current_temperature = 0         # Updated in step()

    if on_pi_hardware:
        # Raspberry Pi software SPI configuration. (For thermocouple)
        CLK = 25
        CS = 24
        DO = 18
        sensor = MAX31855.MAX31855(CLK, CS, DO)

        # Raspberry Pi hardware SPI configuration. (For thermocouple)
        # SPI_PORT = 0
        # SPI_DEVICE = 0
        # sensor = MAX31855.MAX31855(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=5000000))

        i2c = busio.I2C(board.SCL, board.SDA)
        dac = adafruit_mcp4725.MCP4725(i2c)

    # Calculates the temperature based on dni_arr and secs_per_cycle
    def __init__(self, dni_arr, secs_per_cycle):
        self.mutex = Lock()

        # sample every secs_per_cycle since this probably won't run every second
        desired_temp = dni_arr[::secs_per_cycle]

        # multiply by 2 for some reason
        desired_temp = np.multiply(desired_temp, 2)

        # v = (5 / 208) * (DNI) / sqrt(DNI / R)(on each element in the list)
        R = 15
        voltage_ratio = 5/208 # The ratio of the analog control voltage to max voltage into the heater

        for i in range(0, len(desired_temp)):
            desired_temp[i] = voltage_ratio * desired_temp[i] / math.sqrt(desired_temp[i]/R)

        # desired_temp = 8.6*v^2 + 115v (on each element in the list)
        # Estimated calibration equation, analog voltage to Celsius
        for i in range(0, len(desired_temp)):
            desired_temp[i] = 8.6 * math.pow(desired_temp[i], 2) + 115 * desired_temp[i]

        self.desired_temp = desired_temp
        print("DEBUG: [Heater] Constructed")

    # public facing step method
    # spawns a thread and calls the synchronous step_sync helper method
    def step(self):
        print("DEBUG: [Heater] Stepping")
        t1 = Thread(target=self.__step_sync)
        t1.start()

    # private synchronous helper method that runs each time we need to check heater temp
    def __step_sync(self):

        # Stop stepping once we have reached the end of the desired_temp array
        # (for the case where the desired_temp arr is not evenly divisible by secs_per_cycle
        if self.current_step >= len(self.desired_temp) - 1:
            return
        else:
            self.current_step += 1
        if not on_pi_hardware:
            return
        self.mutex.acquire()
        print("DEBUG: [Heater] Stepping for", self.current_step)

        # Read the current temperature
        current_temp = self.sensor.readTempC()
        self.current_temperature = current_temp

        # Calculate the control temperature
        kP = 1000
        ki = 10
        kd = 25

        # control_temperature = desired_temp_c[currentsecond] + kP * error[current reading and current desired
        # temperature] + ki * [sum of all errors] + kd * (this error - previous error)
        ref_temp = self.desired_temp[self.current_step]
        error = ref_temp - current_temp
        control_temperature = ref_temp + kP * error + ki * np.sum(self.errors) + kd * self.errors[len(self.errors) - 1]
        self.errors.append(error)

        # convert control temperature to voltage
        control_voltage = 500 * control_temperature

        # actual dac output (0-4096)
        actual_dac_output = control_voltage / 5 * 4096

        if actual_dac_output > 4096:
            actual_dac_output = 4096
        elif actual_dac_output < 0:
            actual_dac_output = 0

        self.dac.set_voltage(actual_dac_output)

        print("DEBUG: [Heater] Done stepping for", self.current_step)

        self.mutex.release()

    # returns the state of this stepper motor
    def get_state(self):
        return {
            "current_temperature": str(self.current_temperature),
            "reference_temperature": str(self.desired_temp[self.current_step])
        }

    def get_desired_temp_arr(self):
        return self.desired_temp.tolist()
