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
dm = DataManager(glob.glob('D:/Documents/user-data/spotify/StreamingHistory[0-9].json'))

# Top artists by hours_played
top = dm.get_top_n_artists(20)
pg.top_artists_by_hours_streamed(top)


# Filter by hours
hour = dm.get_streamed_hours_by_time_of_day()
pg.streamed_hours_by_time_of_the_day(hour)

# Filter by day of week
day_of_the_week = dm.get_streamed_hours_by_day_of_week()
pg.streamed_hours_by_day_of_the_week(day_of_the_week)

# Cumsum by week (now it has a more decent implementation)
cumsum = dm.get_cumsum_by_week(10)
top_artists = list(dm.get_top_n_artists(10).index)
top_artists.reverse()

pg.cumsum_by_week(cumsum, top_artists)


# Get percent of hours played in top artists
hours = dm.get_percent_hours_played_in_top_artists(20)
pg.pie_top_streamed_artists(hours)

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