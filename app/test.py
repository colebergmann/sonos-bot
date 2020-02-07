#from Robot import Robot
import pandas as pd
#robot = Robot()
try:
    pd.to_datetime("2ok", errors='raise')
    # do something
except ValueError:
    print("invalid")