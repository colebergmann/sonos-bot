from Model import Model
import matplotlib.pyplot as plt

mdl = Model(12, 12, 6200, '06/05/1999') # why is az vertical in the middle of the day? # it inverts after 0 deg
#mdl = Model(34.42,-119.82, 6200, '2019-12-06')

mdl.trim() # trim the plots to one full cycle of apparent_elevation
#mdl.show_plots()

arr = mdl.get_azimuth_arr()
plt.plot(arr)
plt.ylabel('some numbers')
plt.show()
print(len(arr))
