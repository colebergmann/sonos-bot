from Model import Model

#mdl = Model(12, 12, 6200, '06/05/1999') # why is az vertical in the middle of the day? # it inverts after 0 deg
mdl = Model(34.42,-119.82, 6200, '2019-12-06')

mdl.trim() # trim the plots to one full cycle of apparent_elevation
mdl.show_plots()
