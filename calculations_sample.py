from pvlib import solarposition, atmosphere, clearsky
import pandas as pd
import pvlib as pvlib
import matplotlib.pyplot as plt
import pylab

lat = 34.42
lon = -119.842
alt = 6200
date = '2019-12-06'

# Must be longer than a day to make sure we see a continuous cycle
index = pd.date_range(start=date, freq='1s', periods=24*60*60*2)

# solar position data frame (first plot)
solar_df = solarposition.get_solarposition(index, lat, lon)


# this loops thru the elements and picks the left/right indexes for one continuous cycle based on the apparent_elevation
# graph. These values are then used to trim the dataframes so we are only operating on data where the sun is present.
left = -1
right = -1
prev = solar_df.iloc[0]["apparent_elevation"]
for t in solar_df.itertuples():
    curr = t.apparent_elevation
    if left == -1 and prev <= 0 and curr > 0:
        left = t.Index
    if left != -1 and right == -1 and prev >= 0 and curr < 0:
        right = t.Index
        break
    prev = curr

# trim solar df
solar_df = solar_df.drop(solar_df[solar_df.index < left].index)
solar_df = solar_df.drop(solar_df[solar_df.index > right].index)

ax = solar_df.loc[solar_df.index, ['apparent_zenith', 'apparent_elevation', 'azimuth']].plot()
ax.legend(loc=1);
ax.axhline(0, color='darkgray');  # add 0 deg line for sunrise/sunset
ax.axhline(180, color='darkgray');  # add 180 deg line for azimuth at solar noon
ax.set_ylim(-60, 200);  # zoom in, but cuts off full azimuth range
ax.set_xlabel('Time (UTC)');
ax.set_ylabel('(degrees)');

solpos = solarposition.get_solarposition(index, lat, lon)
apparent_zenith = solpos['apparent_zenith']
airmass = atmosphere.get_relative_airmass(apparent_zenith)
pressure = pvlib.atmosphere.alt2pres(alt)
airmass = pvlib.atmosphere.get_absolute_airmass(airmass, pressure)
linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(index, lat, lon)
dni_extra = pvlib.irradiance.get_extra_radiation(index)
sky_df = clearsky.ineichen(apparent_zenith, airmass, linke_turbidity, alt, dni_extra)

#trim sky df
sky_df = sky_df.drop(sky_df[sky_df.index < left].index)
sky_df = sky_df.drop(sky_df[sky_df.index > right].index)

plt.figure();

ax = sky_df.plot()

ax.set_ylabel('Irradiance $W/m^2$');

ax.set_title('Ineichen Clear Sky Model');

ax.legend(loc=2)
pylab.show()