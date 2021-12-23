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
