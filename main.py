import glob

from DataManager import DataManager
from PlotGenerator import PlotGenerator
from ImageGenerator import ImageGenerator

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

# Percent of hours played in top artists
hours = dm.get_percent_hours_played_in_top_artists(20)
pg.pie_top_streamed_artists(hours)

## GENERATE IMAGE
ig = ImageGenerator(size = (1500, 2200))
ig.add_font('title', 'gotham-medium.otf', 60)
ig.add_font('subtitle', 'gotham-medium.otf', 40)
ig.add_font('achievement-title', 'gotham-medium.otf', 24)
ig.add_font('achievement-body', 'gotham-medium.otf', 18)
ig.add_font('icons', 'font-awesome-5-free-solid-900.otf', 58)


# Draw title
ig.write_text('Spotify rewrapped', 'title', (0, 50), horizontal_center=True)

# Draw github corner
ig.paste_image('./github-corner-left.png', (0, 0))

# Draw top played artists plot
ig.paste_image(f'{path}/top-artists.png', (25, 175))

# Draw top played artists plot
ig.paste_image(f'{path}/top-20-pie.png', (750, 175))

# Draw hourly plot
ig.paste_image(f'{path}/hourly-plot.png', (25, 550))

# Draw day of the week plot
ig.paste_image(f'{path}/day-of-the-week-plot.png', (750, 550))

# Draw artists through the year
ig.paste_image(f'{path}/artists-through-the-year.png', (25, 925))

# Draw subtitle
ig.write_text('Achievements', 'subtitle', (25, 1675))

#Achievements
# Christmas spirit
christmas_spirit = dm.all_i_want_for_christmas_is_you()
ig.show_achievement(u'\uf7aa', (25, 1750), (100, 100), 'Christmas spirit', 'I streamed at least 1 hour of\nAll I Want for Christmas Is You by Mariah Carey\n({:.2f}/{:.1f})'.format(christmas_spirit['hours'], 1.0), christmas_spirit['achieved'])

# Halloween
halloween = dm.deffinitive_halloween_experience()
ig.show_achievement(u'\uf717', ((ig.W/2) + 25, 1750), (100, 100), 'The deffinitive Halloween experience', 'I streamed Thriller by Michael Jackson during\nHalloween', halloween)

# Variety
variety = dm.variety_is_the_spice_of_life()
ig.show_achievement(u'\uf200', (25, 1900), (100, 100), 'Variety is the Spice of Life', 'Less than 30% of my total streams are from my\ntop 20 streamed artists', variety)

# Everyday routine
everyday = dm.days_streamed()
ig.show_achievement(u'\uf274', ((ig.W/2) + 25, 1900), (100, 100), 'Everyday routine', 'I streamed at least one track every day of 2021\n({}/{})'.format(everyday['days'], 365), everyday['achieved'])

# Print footer
ig.write_text('Find me on github: https://github.com/willyw0nka/spotify-rewrapped', 'achievement-title', (0, 2100), horizontal_center=True)
ig.write_text('This is not affiliated with Spotify', 'achievement-title', (0, 2150), color=ig.colors['light-gray'], horizontal_center=True)

# Save image
ig.save(f'{path}/spotify-rewrapped.png')
