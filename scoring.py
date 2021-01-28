import datetime
import pandas as pd

from os import path

CSV_DIR = 'csv'
IMAGE_DIR = 'images'

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
        if today not in self.df.index:
            self.df.loc[today] = 0
        self.df.loc[today][name] += score
    
    def get_timeline(self):
        figure = self.df.plot(figsize=(15, 6)).get_figure()
        figure.savefig(self.image_path)
        return self.image_path
        
    def clear(self):
        self.df = pd.DataFrame()
        
    def get_summary_pic(self):
        figure = self.df.sum().plot.barh(figsize=(15, 6)).get_figure()
        figure.savefig(self.image_path)
        return self.image_path