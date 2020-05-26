from Model import Model
import numpy as np
import matplotlib.pyplot as plt

mdl = Model(12, 12, 100, '06/05/1999') # why is az vertical in the middle of the day? # it inverts after 0 deg
#mdl = Model(34.42,-119.82, 6200, '2019-12-06')

mdl.trim() # trim the plots to one full cycle of apparent_elevation
#mdl.show_plots()

mdl.show_plots()

arr = mdl.get_dni_arr()
print(arr)
print(np.multiply(arr, .38))