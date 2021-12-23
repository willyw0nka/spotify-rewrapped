import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as font_manager

class PlotGenerator:
    def __init__(self, path='./', style='./spotify.mplstyle'):
        self.path = path
        font_manager.fontManager.addfont('./gotham-medium.otf')
        mpl.style.use(style)
        mpl.rcParams['font.family'] = 'Gotham Medium'
    
    def top_artists_by_hours_streamed(self, data):
        plt.figure(figsize=(12, 6), dpi=60)
        plt.barh(data.index, data.hours_played)
        plt.suptitle('Top played artists', fontsize=30)
        plt.xlabel('Hours', fontsize=20)
        plt.savefig(f'{self.path}/top-artists.png')
        plt.clf()

    def streamed_hours_by_time_of_the_day(self, data):
        plt.figure(figsize=(12, 6), dpi=60)
        plt.bar(data.index, data.hours_played)
        plt.xticks(range(24), range(24))
        plt.suptitle('Hours played by time of day', fontsize=30)
        plt.savefig(f'{self.path}/hourly-plot.png')
        plt.clf()
    
    def streamed_hours_by_day_of_the_week(self, data):
        plt.figure(figsize=(12, 6), dpi=60)
        days_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Plot morning times
        plt.bar(data['morning'].index, data['morning'].hours_played, label='Morning (6 to 12)')
        # Plot afternoon times
        plt.bar(data['afternoon'].index, data['afternoon'].hours_played, bottom=data['morning'].hours_played, label='Afternoon (13 to 17)')
        # Plot evening times
        plt.bar(data['evening'].index, data['evening'].hours_played, bottom=data['morning'].hours_played+data['afternoon'].hours_played, label='Evening (18 to 21)')
        # Plot night times
        plt.bar(data['night'].index, data['night'].hours_played, bottom=data['morning'].hours_played+data['afternoon'].hours_played+data['evening'].hours_played, label='Night (22 to 5)')
        plt.xticks(range(7), days_labels)
        plt.suptitle('Hours played by day of the week', fontsize=30)
        plt.legend()
        plt.savefig(f'{self.path}/day-of-the-week-plot.png')
        plt.clf()
    
    def cumsum_by_week(self, data, top_artists):
        plt.figure(figsize=(12, 6), dpi=120)
        for artist in top_artists:
            selected_artist = data[data.index == artist]
            plt.plot(range(52), selected_artist.hours_played, label=artist)

        x_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', ' October', 'November', 'December']
        plt.xticks([w for w in range(0, 48) if w % 4 == 0], x_labels, rotation='45')
        plt.legend()
        plt.suptitle('Top played artists through the year', fontsize=15)
        plt.savefig(f'{self.path}/artists-through-the-year.png')
        plt.clf()
    
    def pie_top_streamed_artists(self, data):
        plt.figure(figsize=(12, 6), dpi=60)
        colors = ['#1db954', '#535353']
        explode = (0.1, 0)
        plt.pie(data, colors=colors, autopct='%1.0f%%', textprops={'fontsize': 18}, explode=explode)
        plt.suptitle('My top 20 artists vs others streaming time', fontsize=30)
        plt.savefig(f'{self.path}/top-20-pie.png')
        plt.clf()
