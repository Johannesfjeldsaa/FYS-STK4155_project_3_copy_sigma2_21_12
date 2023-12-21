"""
Written by: Johannes Fjeldså

Resources:
- https://docs.xarray.dev/en/stable/user-guide/plotting.html#plotting
"""

import numpy as np

import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs


from .preproces import Handle_Files


class Plotter:
    def __init__(self):
        self.file_handler = Handle_Files()

    def latitude_formatter(self, x):
        return f"{abs(x):g}\u00b0{'N' if x > 0 else 'S'}"

    def longitude_formatter(self, x):
        if x == 0:
            return f"{abs(x):g}\u00b0"
        elif 0 < x <= 180:
            return f"{abs(x):g}\u00b0E"
        else:
            return f"{abs(x):g}\u00b0W"
    def plot_on_globe(self, data,
                      center_lon=0, center_lat=20,
                      cmap='viridis',
                      title=None, save_fig=False):
        """
        Plot data on a globe.

        Parameters:
        - data (xr.DataArray): The data to be plotted. Horizontal 2D data at a single time step.
        - center_lat (float): The latitude for the center of the plot.
        - center_lon (float): The longitude for the center of the plot.
        - title (str): The title of the plot.
        - save_fig (bool): Whether or not to save the figure.
        """
        p = data.plot(
                subplot_kws=dict(projection=ccrs.Orthographic(center_lon, center_lat), facecolor="gray"),
                transform=ccrs.PlateCarree(),
                cmap=cmap
        )
        p.axes.set_global()
        p.axes.coastlines()

        if title is None:
            title = "Globe plot"
        plt.title(title)

        if save_fig:
            self.file_handler.save_fig(title)

        plt.show()

    def plot_on_map(self, data,
                    cmap="viridis",
                    title=None,
                    save_fig=True):

        fig = plt.figure(figsize=(10, 10 / 1.67))
        ax = plt.axes(projection=ccrs.PlateCarree())

        longitude_ticks = [-180, -120, -60, 0, 60, 120, 180]
        latitude_ticks = [-90, -60, -30, 0, 30, 60, 90]

        ## Map ##
        ax.set_global()
        ax.coastlines()
        ## Plot actual data ##
        contour = ax.contourf(data, transform=ccrs.PlateCarree(), cmap=cmap)
        fig.colorbar(contour, ax=ax)

        ## Set ticks ##
        ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
        ax.set_xticks(longitude_ticks, crs=ccrs.PlateCarree())
        ax.set_yticks(latitude_ticks, crs=ccrs.PlateCarree())
        ax.set_xticklabels([self.longitude_formatter(x) for x in longitude_ticks])
        ax.set_yticklabels([self.latitude_formatter(y) for y in latitude_ticks])
        ax.axhline(y=0,
                   color='blue', linewidth=1.5, linestyle='--')

        ## Set labels ##
        ax.set_xlabel(r'Longitude')
        ax.set_ylabel(r'Latitude')
        if title is None:
            title = "Map plot"
        plt.title(title)

        if save_fig:
            self.file_handler.save_fig(title)

        plt.show()

