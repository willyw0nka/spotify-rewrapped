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

path = 'D:/spotify-unwrapped-plots'

# Configure matplotlib
font_manager.fontManager.addfont('./gotham-medium.otf')
style = './spotify.mplstyle'
mpl.style.use(style)
mpl.rcParams['font.family'] = 'Gotham Medium'

# Read input files
df = pd.DataFrame()
for file in glob.glob('D:/Documents/user-data/spotify/StreamingHistory[0-9].json'):
    print(f"Matched file {file}")
    data_frame = pd.read_json(file)
    df = pd.concat([df, data_frame], axis=0)

# Filter and process data
df['endTime'] = pd.to_datetime(df['endTime'])
df = df[df['endTime'].dt.year == 2021]
df = df[df['msPlayed'] > 10000]

# Add new columns
df['date'] = df.endTime.dt.date
df['month'] = df.endTime.dt.month
df['week'] = df.endTime.dt.isocalendar().week
df['day_of_week'] = df.endTime.dt.dayofweek
df['hour'] = df.endTime.dt.hour
df['part_of_the_day'] = pd.cut(df.hour, bins=[-1, 5, 12, 17, 21, 23], labels=['Night', 'Morning', 'Afternoon', 'Evening', 'Night'], ordered=False)
df['hours_played'] = df.msPlayed / (60 * 60 * 1000)


# Top artists by minutes_played
top = df.groupby("artistName")\
        .agg({"hours_played": np.sum})\
        .sort_values(by=['hours_played'], ascending=True)\
        .tail(20)

plt.figure(figsize=(12, 6), dpi=60)
plt.barh(top.index, top.hours_played)
plt.suptitle('Top played artists by hours')
plt.savefig(f'{path}/top-artists.png')
plt.clf()


# Filter by hours
hour = df.groupby('hour').agg({'hours_played': np.sum})

plt.figure(figsize=(12, 6), dpi=60)
plt.bar(hour.index, hour.hours_played)
plt.xticks(range(24), range(24))
plt.suptitle('Hours played by time of day')
plt.savefig(f'{path}/hourly-plot.png')
plt.clf()

# Filter by day of week
day_of_week = df.groupby(['part_of_the_day', 'day_of_week']).agg({'hours_played': np.sum})
days_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

morning_times = day_of_week.loc['Morning']
afternoon_times = day_of_week.loc['Afternoon']
evening_times = day_of_week.loc['Evening']
night_times = day_of_week.loc['Night']

plt.figure(figsize=(12, 6), dpi=60)

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

# Cumsum by week (spaghetti code, needs to be re done)
artists_list = list(top.index)[10:]

df2 = df[df.artistName.isin(top.index)]
hours_by_week = pd.DataFrame(columns=['week', 'artist_name', 'hours_played'])
for i in range(1,53):
    data = df2[df2.week == i].groupby('artistName').agg({'hours_played': np.sum})
    month_df = pd.DataFrame({'artist_name': data.index, 'week': i, 'hours_played': data.hours_played})
    hours_by_week = hours_by_week.append(month_df)

for artist in artists_list:
    if hours_by_week[hours_by_week.artist_name == artist].shape[0] < 52:
        for w in range(1, 53):
            if not hours_by_week[(hours_by_week.artist_name == artist) & (hours_by_week.week == w)].all(1).any():
                hours_by_week = hours_by_week.append({'artist_name': artist, 'week': w, 'hours_played': 0}, ignore_index=True)

hours_by_week = hours_by_week.set_index('artist_name')

hours_by_week = hours_by_week.sort_values(by=['artist_name', 'week']).groupby('artist_name').cumsum()

plt.figure(figsize=(12, 6), dpi=120)

artists_list.reverse()
for artist in artists_list:
    selected_artist = hours_by_week[hours_by_week.index == artist]
    for i in range(52 - selected_artist.shape[0]):
        selected_artist = selected_artist.append({'artist_name': artist, 'hours_played': 0}, ignore_index=True)
    selected_artist = selected_artist.sort_values(by=['hours_played'])
    plt.plot(range(52), selected_artist.hours_played, label=artist)
x_labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', ' October', 'November', 'December']
plt.xticks([w for w in range(0, 48) if w % 4 == 0], x_labels, rotation='45')
plt.legend()
plt.suptitle('Top played artists through the year')
plt.savefig(f'{path}/artists-through-the-year.png')
plt.clf()

# Get percent of hours played in top artists
artists = list(top.index)
total_hours = df.hours_played.sum()
top_hours = df[df.artistName.isin(artists)].hours_played.sum()

plt.figure(figsize=(12, 6), dpi=60)
data = [top_hours, total_hours - top_hours]
colors = ['#1db954', '#535353']
explode = (0.1, 0)
plt.pie(data, colors=colors, autopct='%1.0f%%', textprops={'fontsize': 18}, explode=explode)
plt.suptitle('My top 20 artists vs others streaming time')
plt.savefig(f'{path}/top-20-pie.png')
plt.clf()

# Achievements
# Hours streaming all i want for christmas is you
all_i_want_for_christmas_is_you = df[df.trackName == 'All I Want for Christmas Is You'].groupby('trackName')\
                                                                .agg({'hours_played': np.sum})\
                                                                .hours_played[0] # > 1

# The definitive halloween experience
streamed_thriller = df[(df.trackName == 'Thriller') & (df.artistName == 'Michael Jackson')]

# Days that used
streamed_every_day = df.groupby('date').size().size # == 365

# Songs in top 100 spotify 2021

# Streamed enemy from arcane
# :(

# Variety is the Spice of Life
variety_is_the_spice_of_life = top_hours / total_hours # < 0.25

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