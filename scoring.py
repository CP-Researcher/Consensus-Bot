import datetime
import pandas as pd

import os
from os import path

CSV_DIR = 'csv'
IMAGE_DIR = 'images'

for directory in [CSV_DIR, IMAGE_DIR]:
    if not path.isdir(directory):
        os.makedirs(directory)


class Board:
    
    def __init__(self, channel_id):
        self.file_path = f'{CSV_DIR}/{channel_id}.csv'
        self.image_path = f'{IMAGE_DIR}/{channel_id}.png'
        
        if path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path, index_col=0)
            self.df.index = pd.to_datetime(self.df.index)
        else:
            self.df = pd.DataFrame()
            
    def __del__(self):
        self.df.to_csv(self.file_path)
    
    def add_member(self, name):
        self.df[name] = 0
        
    def add_score(self, name, score):
        today = pd.to_datetime(datetime.date.today())
        name = str(name)
        
        # Insert row if not exist
        if today not in self.df.index:
            self.df.loc[today] = 0
        
        # Insert column if not exist
        if name not in self.df.columns:
            self.add_member(name)
        
        self.df.loc[today, name] += score
    
    def get_timeline(self):
        figure = self.df.plot(figsize=(15, 6)).get_figure()
        figure.savefig(self.image_path)
        return self.image_path
        
    def clear(self):
        self.df = pd.DataFrame()
        
    def get_summary_pic(self, user_map):
        df = self.df.rename(columns=user_map)
        figure = df.sum().plot.barh(figsize=(15, 6)).get_figure()
        figure.savefig(self.image_path)
        return self.image_path