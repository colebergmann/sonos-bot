

feedback_temp_c = [20, 25, 20] # Read in the temperature
desired_temp_c = [21, 21, 21, 21] # DNI Value (multiply by a constant (2 as placeholder)), then we want to convert to voltage in

# Voltage equation:
r=15
DNI = the number thing above (multiplied by 2)
v = (5/208) * (DNI) / sqrt(DNI/R) (on each element in the list)
desired_temp = 8.6*v^2 + 115v (on each element in the list)



# as each iteration goes by irl

# set previous error (and this error) at 0 initially

kP = 1000
ki = 10
kd = 25


control_temperature = desired_temp_c[currentsecond] + kP * error[current reading and current desired temperature] + ki * [sum of all errors] + kd * (this error - previous error)

# convert to voltage
control_voltage = 500 * control_temperature

# send out the voltage

# Save the error and the temperatures coming in