from TurntableMotor import TurntableMotor
from threading import Event, Thread
from Model import Model
from datetime import datetime
from datetime import timedelta
from RobotTimer import RobotTimer


class Robot:
    turntable = TurntableMotor()
    status = "ready"  # status = ready/calculating/resetting/running/done
    model = None
    lat = 0
    lon = 0
    elevation = 0
    date_param = 0
    azimuth_arr = None
    start_date = datetime.now()
    current_seconds = 0
    total_seconds = 1
    timer = None

    SECS_PER_CYCLE = 300    # time each cycle accounts for
    CYCLE_PERIOD = 2        # time between cycles

    def __init__(self):
        print("DEBUG: [ROBOT] Object instantiated")
        #self.calculate(5, 5, 2000, '12/12/2009')

    def calculate(self, lat, lon, elevation, date):
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
            self.total_seconds = len(self.azimuth_arr)
            self.start_date = datetime.now()

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
        self.status = "running"

    def run_timer(self):
        self.turntable.set_degrees(self.azimuth_arr[self.current_seconds])
        self.current_seconds += self.SECS_PER_CYCLE
        if self.current_seconds > len(self.azimuth_arr):
            self.timer.event.set()
            self.status = "completed"

    # returns json format of Robot's current state
    def get_state(self):
        return {
            "status": self.status,
            #"rotational_motor": self.rotational_motor.get_state(),
            "lat": self.lat,
            "lon": self.lon,
            "elevation": self.elevation,
            "date_param": self.date_param,
            "started_date": self.start_date.strftime("%-I:%M %p, %A %b %d"),
            "completion_date": self.getCompletionDate(),
            "time_elapsed": self.seconds_to_string(self.current_seconds),
            "time_remaining": self.seconds_to_string(self.total_seconds - self.current_seconds),
            "percentage_complete": int((self.current_seconds / self.total_seconds)*100),
            "turntable": self.turntable.get_state()
        }

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
        self.status = "ready"

    def get_graph(self):

        return {
            "y": self.azimuth_arr[::20].flatten('F').tolist(),
            "type": "scatter"
        }

    def getCompletionDate(self):
        if self.status == "running":
            return (datetime.now() + timedelta(seconds=self.total_seconds - self.current_seconds)).strftime("%-I:%M %p, %A %b %d")
        else:
            return "-"
