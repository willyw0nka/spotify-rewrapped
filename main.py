import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import glob
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.font_manager as font_manager
from datetime import date

from DataManager import DataManager
from PlotGenerator import PlotGenerator

path = 'D:/spotify-unwrapped-plots'

# Configure matplotlib
pg = PlotGenerator(path=path, style='./spotify.mplstyle')

font_manager.fontManager.addfont('./gotham-medium.otf')
style = './spotify.mplstyle'
mpl.style.use(style)
mpl.rcParams['font.family'] = 'Gotham Medium'

dm = DataManager(glob.glob('D:/Documents/user-data/spotify/StreamingHistory[0-9].json'))

# Top artists by minutes_played
top = dm.get_top_n_artists(20)

plt.figure(figsize=(12, 6), dpi=60)
plt.barh(top.index, top.hours_played)
plt.suptitle('Top played artists by hours')
plt.savefig(f'{path}/top-artists.png')
plt.clf()


# Filter by hours
hour = dm.get_streamed_hours_by_time_of_day()

plt.figure(figsize=(12, 6), dpi=60)
plt.bar(hour.index, hour.hours_played)
plt.xticks(range(24), range(24))
plt.suptitle('Hours played by time of day')
plt.savefig(f'{path}/hourly-plot.png')
plt.clf()

# Filter by day of week
day_of_week = dm.get_streamed_hours_by_day_of_week()

morning_times = day_of_week['morning']
afternoon_times = day_of_week['afternoon']
evening_times = day_of_week['evening']
night_times = day_of_week['night']


plt.figure(figsize=(12, 6), dpi=60)
days_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Plot morning times
plt.bar(morning_times.index, morning_times.hours_played, label='Morning (6 to 12)')
# Plot afternoon times
plt.bar(afternoon_times.index, afternoon_times.hours_played, bottom=morning_times.hours_played, label='Afternoon (13 to 17)')
# Plot evening times
plt.bar(evening_times.index, evening_times.hours_played, bottom=morning_times.hours_played+afternoon_times.hours_played, label='Evening (18 to 21)')
# Plot night times
plt.bar(night_times.index, night_times.hours_played, bottom=morning_times.hours_played+afternoon_times.hours_played+evening_times.hours_played, label='Night (22 to 5)')
plt.xticks(range(7), days_labels)
plt.suptitle('Hours played by day of the week')
plt.legend()
plt.savefig(f'{path}/day-of-the-week-plot.png')
plt.clf()

# Cumsum by week (now it has a more decent implementation)
cumsum = dm.get_cumsum_by_week(10)
top_artists = list(dm.get_top_n_artists(10).index)
top_artists.reverse()

plt.figure(figsize=(12, 6), dpi=120)
for artist in top_artists:
    print(artist)
    selected_artist = cumsum[cumsum.index == artist]
    plt.plot(range(52), selected_artist.hours_played, label=artist)

x_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', ' October', 'November', 'December']
plt.xticks([w for w in range(0, 48) if w % 4 == 0], x_labels, rotation='45')
plt.legend()
plt.suptitle('Top played artists through the year')
plt.savefig(f'{path}/artists-through-the-year.png')
plt.clf()

# Get percent of hours played in top artists
hours = dm.get_percent_hours_played_in_top_artists(20)

plt.figure(figsize=(12, 6), dpi=60)
colors = ['#1db954', '#535353']
explode = (0.1, 0)
plt.pie(hours, colors=colors, autopct='%1.0f%%', textprops={'fontsize': 18}, explode=explode)
plt.suptitle('My top 20 artists vs others streaming time')
plt.savefig(f'{path}/top-20-pie.png')
plt.clf()

# Achievements
# Hours streaming all i want for christmas is you
# all_i_want_for_christmas_is_you = df[df.trackName == 'All I Want for Christmas Is You'].groupby('trackName')\
#                                                                 .agg({'hours_played': np.sum})\
#                                                                 .hours_played[0] # > 1

# # The definitive halloween experience
# streamed_thriller = df[(df.trackName == 'Thriller') & (df.artistName == 'Michael Jackson')]

# # Days that used
# streamed_every_day = df.groupby('date').size().size # == 365

# # Songs in top 100 spotify 2021

# # Streamed enemy from arcane
# # :(

# # Variety is the Spice of Life
# variety_is_the_spice_of_life = top_hours / total_hours # < 0.25

## GENERATE IMAGE
W, H = (1500, 2000)
title = 'Spotify rewrapped'

background = Image.new('RGB', (W, H), color = (25, 20, 20))
bg_w, bg_h = background.size
title_font = ImageFont.truetype('gotham-medium.otf', 48)

# Draw title
draw = ImageDraw.Draw(background)
w, h = draw.textsize(title, font=title_font)
draw.text(((W-w)/2, 25), title,(255,255,255),font=title_font)

# Draw top played artists plot
plot = Image.open(f'{path}/top-artists.png', 'r')
background.paste(plot, (25, 125))

# Draw top played artists plot
plot = Image.open(f'{path}/top-20-pie.png', 'r')
background.paste(plot, (750, 125))

# Draw hourly plot
plot = Image.open(f'{path}/hourly-plot.png', 'r')
background.paste(plot, (25, 500))

# Draw day of the week plot
plot = Image.open(f'{path}/day-of-the-week-plot.png', 'r')
background.paste(plot, (750, 500))

# Draw artists through the year
plot = Image.open(f'{path}/artists-through-the-year.png', 'r')
background.paste(plot, (25, 1000))

# Save image
background.save(f'{path}/spotify-rewrapped.png')