"""spotify_rewrapped module, contains SpotifyRewrapped class."""

import glob
import os

from data_manager import DataManager
from plot_generator import PlotGenerator
from image_generator import ImageGenerator

class SpotifyRewrapped:
    """Spotify Rewrapped. Main class"""

    def __init__(self, path: str, output: str, timezone: str = 'UTC'):
        """Init method. Calls generate and cleanup methods.

        Args:
            path (str): Path where the StreamingHistory.json are located.
            output (str): Path where result png will be generated.
            timezone (str): Indicates the timezone to use. Default is 'UTC'.
        """
        self.path = path
        self.output = output
        self.timezone = timezone
        self.generate()
        self.cleanup()

    def generate(self):
        """Calls the PlotGenerator, DataManager and ImageGenerator to create the result.
        """
        # Configure matplotlib
        pg = PlotGenerator(path=self.path,
                           style='./resources/spotify.mplstyle',
                           font='./resources/gotham-medium.otf')
        dm = DataManager(glob.glob(f'{self.path}/StreamingHistory[0-9].json'), timezone=self.timezone)

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
        ig.add_font('title', './resources/gotham-medium.otf', 60)
        ig.add_font('subtitle', './resources/gotham-medium.otf', 40)
        ig.add_font('achievement-title', './resources/gotham-medium.otf', 24)
        ig.add_font('achievement-body', './resources/gotham-medium.otf', 18)
        ig.add_font('icons', './resources/font-awesome-5-free-solid-900.otf', 58)

        # Draw title
        ig.write_text('Spotify rewrapped', 'title', (0, 50), horizontal_center=True)

        # Draw github corner
        ig.paste_image('./resources/github-corner-left.png', (0, 0))

        # Draw top played artists plot
        ig.paste_image(f'{self.path}/top-artists.png', (25, 175))

        # Draw top played artists plot
        ig.paste_image(f'{self.path}/top-20-pie.png', (750, 175))

        # Draw hourly plot
        ig.paste_image(f'{self.path}/hourly-plot.png', (25, 550))

        # Draw day of the week plot
        ig.paste_image(f'{self.path}/day-of-the-week-plot.png', (750, 550))

        # Draw artists through the year
        ig.paste_image(f'{self.path}/artists-through-the-year.png', (25, 925))

        # Draw subtitle
        ig.write_text('Achievements', 'subtitle', (25, 1675))

        #Achievements
        # Christmas spirit
        christmas_spirit = dm.all_i_want_for_christmas_is_you()
        ig.show_achievement('\uf7aa', (25, 1750), (100, 100), 'Christmas spirit',
                            'I streamed at least 1 hour of\n'
                            'All I Want for Christmas Is You by Mariah Carey\n'
                            '({:.2f}/{:.1f})'.format(christmas_spirit['hours'], 1.0),
                            christmas_spirit['achieved'])

        # Halloween
        halloween = dm.deffinitive_halloween_experience()
        ig.show_achievement('\uf717', ((ig.W/2) + 25, 1750), (100, 100),
                            'The deffinitive Halloween experience',
                            'I streamed Thriller by Michael Jackson during\n'
                            'Halloween', halloween)

        # Variety
        variety = dm.variety_is_the_spice_of_life()
        ig.show_achievement('\uf200', (25, 1900), (100, 100),
                            'Variety is the Spice of Life',
                            'Less than 30% of my total streams are from my'
                            '\ntop 20 streamed artists', variety)

        # Everyday routine
        everyday = dm.days_streamed()
        ig.show_achievement('\uf274', ((ig.W/2) + 25, 1900), (100, 100),
                            'Everyday routine',
                            'I streamed at least one track every day of 2021'
                            '\n({}/{})'.format(everyday['days'], 365), everyday['achieved'])

        # Pareto principle
        pareto = dm.pareto_principle()
        ig.show_achievement('\uf6fc', (25, 2050), (100, 100),
                            'Pareto principle confirmed',
                            'More than 80% of my total streams are from my'
                            '\ntop 20% streamed artists'
                            '\n({:.2f}%)'.format(pareto * 100,), pareto  > 0.8)

        # Print footer
        ig.write_text('Find me on github: https://github.com/willyw0nka/spotify-rewrapped',
                      'achievement-title', (0, 2250), horizontal_center=True)
        ig.write_text('This is not affiliated with Spotify', 'achievement-title',
                      (0, 2300), color=ig.colors['light-gray'], horizontal_center=True)

        # Save image
        ig.save(self.output)
        print('Image generated successfully!')

    def cleanup(self):
        """Removes all the intermediate png generated files.
        """
        # Cleanup
        os.remove(f'{self.path}/top-artists.png')
        os.remove(f'{self.path}/top-20-pie.png')
        os.remove(f'{self.path}/hourly-plot.png')
        os.remove(f'{self.path}/day-of-the-week-plot.png')
        os.remove(f'{self.path}/artists-through-the-year.png')
