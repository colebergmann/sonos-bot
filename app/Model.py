from pvlib import solarposition, atmosphere, clearsky
import pandas as pd
import pvlib as pvlib
import matplotlib.pyplot as plt
import pylab


class Model:

    solar_df = None
    sky_df = None

    # constructor
    # calculate the models and store in dataframes
    def __init__(self, lat, lon, elevation, date):
        # Must be longer than a day to make sure we see a continuous cycle
        index = pd.date_range(start=date, freq='1s', periods=24 * 60 * 60 * 2)

        # Generate solar position df
        self.solar_df = solarposition.get_solarposition(index, lat, lon)

        # generate sky df
        solpos = solarposition.get_solarposition(index, lat, lon)
        apparent_zenith = solpos['apparent_zenith']
        airmass = atmosphere.get_relative_airmass(apparent_zenith)
        pressure = pvlib.atmosphere.alt2pres(elevation)
        airmass = pvlib.atmosphere.get_absolute_airmass(airmass, pressure)
        linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(index, lat, lon)
        dni_extra = pvlib.irradiance.get_extra_radiation(index)
        self.sky_df = clearsky.ineichen(apparent_zenith, airmass, linke_turbidity, elevation, dni_extra)

    # bound dataframes to only one cycle of the sun being up
    def trim(self):
        # this loops thru the elements and picks the left/right indexes for one continuous cycle based on the
        # apparent_elevation graph. These values are then used to trim the dataframes so we are only operating on
        # data where the sun is present.

        left = -1
        right = -1
        prev = self.solar_df.iloc[0]["apparent_elevation"]
        for t in self.solar_df.itertuples():
            curr = t.apparent_elevation
            if left == -1 and prev <= 0 and curr > 0:
                left = t.Index
            if left != -1 and right == -1 and prev >= 0 and curr < 0:
                right = t.Index
                break
            prev = curr

        # trim solar df
        self.solar_df = self.solar_df.drop(self.solar_df[self.solar_df.index < left].index)
        self.solar_df = self.solar_df.drop(self.solar_df[self.solar_df.index > right].index)
        # trim sky df
        self.sky_df = self.sky_df.drop(self.sky_df[self.sky_df.index < left].index)
        self.sky_df = self.sky_df.drop(self.sky_df[self.sky_df.index > right].index)

        # fix the bullshit
        prev = self.solar_df.iloc[0]["azimuth"]
        for t in self.solar_df.itertuples():
            curr = t.apparent_elevation
            if left == -1 and prev <= 0 and curr > 0:
                left = t.Index
            if left != -1 and right == -1 and prev >= 0 and curr < 0:
                right = t.Index
                break
            prev = curr


    def show_plots(self):
        # graph solar position df
        ax = self.solar_df.loc[self.solar_df.index, ['apparent_zenith', 'apparent_elevation', 'azimuth']].plot()
        ax.legend(loc=1);
        ax.axhline(0, color='darkgray');  # add 0 deg line for sunrise/sunset
        ax.axhline(180, color='darkgray');  # add 180 deg line for azimuth at solar noon
        ax.set_ylim(-60, 200);  # zoom in, but cuts off full azimuth range
        ax.set_xlabel('Time (UTC)');
        ax.set_ylabel('(degrees)');

        plt.figure();

        ax = self.sky_df.plot()

        ax.set_ylabel('Irradiance $W/m^2$');

        ax.set_title('Ineichen Clear Sky Model');

        ax.legend(loc=2)
        pylab.show()

    # returns array of azimuth values at every second
    def get_azimuth_arr(self):
        arr = self.solar_df[['azimuth']].to_numpy()

        # invert for cases where graph jumps from 0 to 360
        invert = False
        for i in range(1, len(arr)):
            delta = abs(arr[i] - arr[i-1])
            # if the graph jumps, then correct the values
            if delta > 300 and not invert:
                invert = True
            if invert:
                arr[i] = arr[i] - 360

        # normalize to start at zero
        for i in range(1, len(arr)):
            arr[i] = arr[i] - arr[0]
        arr[0] = 0
        return arr
