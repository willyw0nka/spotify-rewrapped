"""This module contains the PlotGenerator class which is responsible of generating
the individual plots."""
import matplotlib.pyplot as plt
import matplotlib as mpl
from  matplotlib import font_manager
import pandas as pd

class PlotGenerator:
    """PlotGenerator. Contains the methods that allow creating the different plots."""
    def __init__(self, path='./',
                 style='./resources/spotify.mplstyle',
                 font='./resources/gotham-medium.otf'):
        """Initial configuration.

        Args:
            path (str, optional): Path where the plot images will be stored. Defaults to './'.
            style (str, optional): MatPlotLib style. Defaults to './resources/spotify.mplstyle'.
            font (str, optional): Font that MatPlotLib will use. Defaults to './resources/gotham-medium.otf'.
        """        
        self.path = path
        font_manager.fontManager.addfont(font)
        mpl.style.use(style)
        mpl.rcParams['font.family'] = 'Gotham'

    def top_artists_by_hours_streamed(self, data: pd.DataFrame):
        """Generates a barh plot showing the top 20 top streamed artists.

        Args:
            data (pd.DataFrame): Input data.
        """
        plt.figure(figsize=(12, 6), dpi=60)
        plt.barh(data.index, data.hours_played)
        plt.suptitle('Top played artists', fontsize=30)
        plt.xlabel('Hours', fontsize=20)
        plt.savefig(f'{self.path}/top-artists.png')
        plt.clf()

    def streamed_hours_by_time_of_the_day(self, data: pd.DataFrame):
        """Generates a bar plot showing the streamed hours by time of the day.

        Args:
            data (pd.DataFrame): Input data.
        """
        plt.figure(figsize=(12, 6), dpi=60)
        plt.bar(data.index, data.hours_played)
        plt.xticks(range(24), range(24))
        plt.suptitle('Hours played by time of day', fontsize=30)
        plt.savefig(f'{self.path}/hourly-plot.png')
        plt.clf()

    def streamed_hours_by_day_of_the_week(self, data: pd.DataFrame):
        """Generates a bar plot showing the streamed hours day of the week.

        Args:
            data (pd.DataFrame): Input data.
        """
        plt.figure(figsize=(12, 6), dpi=60)
        days_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        # Plot morning times
        plt.bar(data['morning'].index, data['morning'].hours_played, label='Morning (6 to 12)')
        # Plot afternoon times
        plt.bar(data['afternoon'].index,
                data['afternoon'].hours_played,
                bottom=data['morning'].hours_played,
                label='Afternoon (13 to 17)')
        # Plot evening times
        plt.bar(data['evening'].index,
                data['evening'].hours_played,
                bottom=data['morning'].hours_played+data['afternoon'].hours_played,
                label='Evening (18 to 21)')
        # Plot night times
        plt.bar(data['night'].index, data['night'].hours_played,
                bottom=data['morning'].hours_played +
                data['afternoon'].hours_played +
                data['evening'].hours_played,
                label='Night (22 to 5)')
        plt.xticks(range(7), days_labels)
        plt.suptitle('Hours played by day of the week', fontsize=30)
        plt.legend()
        plt.savefig(f'{self.path}/day-of-the-week-plot.png')
        plt.clf()

    def cumsum_by_week(self, data: pd.DataFrame, top_artists: list):
        """Generates a plot showing the cumulative streamed hours of your top 10
        top streamed artists, xtick is weeks.

        Args:
            data (pd.DataFrame): Input data.
            top_artists (list): List of artist name that will be included on the plot.
        """
        plt.figure(figsize=(12, 6), dpi=120)
        for artist in top_artists:
            selected_artist = data[data.index == artist]
            plt.plot(range(52), selected_artist.hours_played, label=artist)

        x_labels = ['New year', 'January', 'February', 'March', 'April', 'May','June',
                    'July', 'August', 'September', ' October', 'November', 'December']
        x_ticks = [0, 5, 9, 14, 18, 23, 27, 31, 36, 40, 45, 49, 53]
        plt.xticks(x_ticks, x_labels, rotation='45')
        plt.legend()
        plt.suptitle('Top played artists through the year', fontsize=15)
        plt.savefig(f'{self.path}/artists-through-the-year.png')
        plt.clf()

    def pie_top_streamed_artists(self, data: list):
        """Generates a pie plot showing the percentage of streamed hours that pertain
        to your top 20 top streamed artists.

        Args:
            data (list): Input data.
        """
        plt.figure(figsize=(12, 6), dpi=60)
        colors = ['#1db954', '#535353']
        explode = (0.1, 0)
        plt.pie(data, colors=colors, autopct='%1.0f%%', textprops={'fontsize': 36}, explode=explode)
        plt.suptitle('My top 20 artists vs others streaming time', fontsize=30)
        plt.savefig(f'{self.path}/top-20-pie.png')
        plt.clf()
