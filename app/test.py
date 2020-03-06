#from Robot import Robot
import pandas as pd
from Model import Model

mdl = Model(12, 12, 6200, '06/05/1999')
#mdl = Model(34.42,-119.82, 6200, '2019-12-06')

# wtf why is az vertical in the middle of the day?

mdl.trim()
mdl.show_plots()
for i in mdl.get_azimuth_arr():
    print(i)

