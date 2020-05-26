from TurntableMotor import TurntableMotor
from ArmMotor import ArmMotor
from threading import Event, Thread
from Model import Model
from datetime import datetime
from datetime import timedelta
from RobotTimer import RobotTimer
from Heater import Heater
import numpy as np
from flask import jsonify


class Robot:

    SECS_PER_CYCLE = 300  # time each cycle accounts for
    CYCLE_PERIOD = 2  # time between cycles (in seconds)

    def __init__(self):
        print("DEBUG: [ROBOT] Object instantiated")
        self.turntable_motor = TurntableMotor()
        self.arm_motor = ArmMotor()
        self.heater = None
        self.status = "ready"  # status = ready/calculating/resetting/running/done
        self.model = None
        self.lat = 0
        self.lon = 0
        self.elevation = 0
        self.date_param = 0
        self.start_date = datetime.now()
        self.current_seconds = 0
        self.total_seconds = 1
        self.timer = None
        self.speaker_color = "black"  # or "white"

        self.azimuth_arr = None
        self.elevation_arr = None
        self.dni_arr = None

    # Create the Model object based off the given parameters and calculate the data arrays for each motor
    def calculate(self, lat, lon, elevation, date, speaker_color):
        self.status = "calculating"

        # make sure the calculations are successful. if not, kick user back to params page
        try:
            model = Model(lat, lon, elevation, date)
            model.trim()
            self.lat = lat
            self.lon = lon
            self.elevation = elevation
            self.date_param = date
            self.azimuth_arr = model.get_azimuth_arr()
            self.elevation_arr = model.get_apparent_elevation_arr()
            self.dni_arr =model.get_dni_arr()
            self.total_seconds = len(self.azimuth_arr)
            self.start_date = datetime.now()
            self.speaker_color = speaker_color

            # Initialize the heater
            self.heater = Heater(self.dni_arr, self.SECS_PER_CYCLE)

            # multiply dni by *.38 if its white
            if self.speaker_color == "white":
                self.dni_arr = np.multiply(self.dni_arr, 0.38)

            # make sure all 3 data arrays are equal length
            assert(len(self.azimuth_arr) == len(self.elevation_arr))
            assert (len(self.azimuth_arr) == len(self.dni_arr))

            #commence the timer!
            self.run_timer()
            self.timer = RobotTimer(self.CYCLE_PERIOD, self.run_timer)
        except Exception as e:
            print(e)
            self.status = "ready"
            return

        # calculations have finished, move on to resetting the robot
        self.reset()

    def reset(self):
        self.status = "resetting"
        #t1 = Thread(target=self.rotational_motor.reset)
        #t1.start()
        #t1.join()
        self.arm_motor.reset_motor()
        self.status = "running"

    def run_timer(self):
        self.turntable_motor.set_degrees(self.azimuth_arr[self.current_seconds])
        self.arm_motor.set_degrees(self.elevation_arr[self.current_seconds])
        self.current_seconds += self.SECS_PER_CYCLE
        self.heater.step()
        if self.current_seconds > len(self.azimuth_arr):
            self.timer.event.set()
            self.status = "completed"

    # returns json format of Robot's current state
    def get_state(self):
        state = {
            "status": self.status,
            "lat": self.lat,
            "lon": self.lon,
            "elevation": self.elevation,
            "date_param": self.date_param,
            "started_date": self.start_date.strftime("%-I:%M %p, %A %b %d"),
            "completion_date": self.getCompletionDate(),
            "time_elapsed": self.seconds_to_string(self.current_seconds),
            "time_remaining": self.seconds_to_string(self.total_seconds - self.current_seconds),
            "percentage_complete": int((self.current_seconds / self.total_seconds)*100),
            "turntable": self.turntable_motor.get_state(),
            "arm_motor": self.arm_motor.get_state(),
            "speaker_color": self.speaker_color,
        }
        if self.heater is not None:
            state["heater"] = self.heater.get_state()

        return state

    def get_status(self):
        return self.status

    def pause(self):
        if self.status == "running":
            self.status = "paused"
            self.timer.stop()
            self.timer = None

    def resume(self):
        if self.status == "paused":
            self.status = "running"
            self.timer = RobotTimer(self.CYCLE_PERIOD, self.run_timer)


    def seconds_to_string(self, secs):
        result = ""
        hrs = secs / 60 / 60
        if hrs > 0:
            result += str(int(hrs)) + "h "
        result += str(int(secs / 60) % 60) + "m"
        return result

    def cancel(self):
        self.timer.stop()
        if self.timer is not None:
            self.timer = None
        self.status = "ready"

    def get_azimuth_graph(self):
        return {
            "y": self.azimuth_arr[::60].flatten('F').tolist(),
            "type": "scatter"
        }

    def get_elevation_graph(self):
        return {
            "y": self.elevation_arr[::60].flatten('F').tolist(),
            "type": "scatter"
        }

    def get_dni_graph(self):
        return {
            "y": self.dni_arr[::60].flatten('F').tolist(),
            "type": "scatter"
        }

    def get_temperature_graph(self):
        scale = int(60/self.SECS_PER_CYCLE)
        if (scale ==  0):
            scale = 1
        return {
            "y": np.array(self.heater.get_desired_temp_arr())[::scale].flatten('F').tolist(),
            "type": "scatter"
        }

    def getCompletionDate(self):
        if self.status == "running":
            return (datetime.now() + timedelta(seconds=self.total_seconds - self.current_seconds)).strftime("%-I:%M %p, %A %b %d")
        else:
            return "-"
