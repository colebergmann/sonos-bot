from pvlib import solarposition, atmosphere, clearsky
from pandas import Timestamp
import pandas as pd
import pvlib as pvlib
import matplotlib.pyplot as plt
import pytz
import pylab
import tables

lat = 39.1976;
lon = -120.2354;
alt =6200;

index = pd.date_range(start='2019-12-06', tz='UTC', freq='1s', periods=24*60*60)
print(index)

solar_position_notz = solarposition.get_solarposition(index, lat, lon)

print(solar_position_notz)

ax = solar_position_notz.loc[solar_position_notz.index, ['apparent_zenith', 'apparent_elevation', 'azimuth']].plot()
ax.legend(loc=1);

ax.axhline(0, color='darkgray');  # add 0 deg line for sunrise/sunset

ax.axhline(180, color='darkgray');  # add 180 deg line for azimuth at solar noon

ax.set_ylim(-60, 200);  # zoom in, but cuts off full azimuth range

ax.set_xlabel('Time (UTC)');

ax.set_ylabel('(degrees)');
#pylab.show()



# kill me
solpos = solarposition.get_solarposition(index, lat, lon)
apparent_zenith = solpos['apparent_zenith']
airmass = atmosphere.get_relative_airmass(apparent_zenith)
pressure = pvlib.atmosphere.alt2pres(alt)
airmass = pvlib.atmosphere.get_absolute_airmass(airmass, pressure)
linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(index, lat, lon)
dni_extra = pvlib.irradiance.get_extra_radiation(index)
ineichen = clearsky.ineichen(apparent_zenith, airmass, linke_turbidity, alt, dni_extra)
plt.figure();

ax = ineichen.plot()

ax.set_ylabel('Irradiance $W/m^2$');

ax.set_title('Ineichen Clear Sky Model');

ax.legend(loc=2)
pylab.show()