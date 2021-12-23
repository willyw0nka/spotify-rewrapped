import numpy as np
import pandas as pd

class DataManager:
    def __init__(self, files=None):
        # Read input files
        self.df = pd.DataFrame()
        for file in files:
            print(f"Matched file {file}")
            data_frame = pd.read_json(file)
            self.df = pd.concat([self.df, data_frame], axis=0)
        
        # Filter and process data
        self.df.endTime = pd.to_datetime(self.df.endTime)
        self.df = self.df[self.df.endTime.dt.year == 2021]
        self.df = self.df[self.df.msPlayed > 10000]
        
        # Add new columns
        self.df['date'] = self.df.endTime.dt.date
        self.df['month'] = self.df.endTime.dt.month
        self.df['week'] = self.df.endTime.dt.isocalendar().week
        self.df['day_of_week'] = self.df.endTime.dt.dayofweek
        self.df['hour'] = self.df.endTime.dt.hour
        self.df['part_of_the_day'] = pd.cut(self.df.hour, bins=[-1, 5, 12, 17, 21, 23], labels=['Night', 'Morning', 'Afternoon', 'Evening', 'Night'], ordered=False)
        self.df['hours_played'] = self.df.msPlayed / (60 * 60 * 1000)

    def get_top_n_artists(self, n):
        return self.df.groupby('artistName')\
                    .agg({'hours_played': np.sum})\
                    .sort_values(by=['hours_played'], ascending=True)\
                    .tail(n)
                    
    def get_streamed_hours_by_time_of_day(self):
        return self.df.groupby('hour').agg({'hours_played': np.sum})

    def get_streamed_hours_by_day_of_week(self):
        day_of_week = self.df.groupby(['part_of_the_day', 'day_of_week']).agg({'hours_played': np.sum})

        return {'morning': day_of_week.loc['Morning'],
                'afternoon': day_of_week.loc['Afternoon'],
                'evening': day_of_week.loc['Evening'],
                'night': day_of_week.loc['Night']}
    
    def get_percent_hours_played_in_top_artists(self, n):
        artists = list(self.get_top_n_artists(n).index)
        total_hours = self.df.hours_played.sum()
        top_hours = self.df[self.df.artistName.isin(artists)].hours_played.sum()
        
        return [top_hours, total_hours - top_hours]
    
    def get_cumsum_by_week(self, n):
        top_artists = self.get_top_n_artists(n)
        
        df2 = self.df[self.df.artistName.isin(top_artists.index)]
        hours_by_week = pd.DataFrame(columns=['week', 'artist_name', 'hours_played'])
        for i in range(1,53):
            # Join all weekly streams into one by artist
            data = df2[df2.week == i].groupby('artistName').agg({'hours_played': np.sum})
            week_df = pd.DataFrame({'artist_name': data.index, 'week': i, 'hours_played': data.hours_played})
            hours_by_week = hours_by_week.append(week_df)
        
        # Fill missing weeks
        for artist in list(top_artists.index):
            if hours_by_week[hours_by_week.artist_name == artist].shape[0] < 52:
                for w in range(1, 53):
                    if not hours_by_week[(hours_by_week.artist_name == artist) & (hours_by_week.week == w)].all(1).any():
                        hours_by_week = hours_by_week.append({'artist_name': artist, 'week': w, 'hours_played': 0}, ignore_index=True)
        
        hours_by_week = hours_by_week.set_index('artist_name')\
                                    .sort_values(by=['artist_name', 'week'])\
                                    .groupby('artist_name')\
                                    .cumsum()
        
        return hours_by_week