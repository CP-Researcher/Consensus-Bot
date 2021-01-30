import os
import pandas as pd

from os import path
from datetime import datetime

CSV_DIR = 'csv'
FILE_NAME = 'queue'

if not path.isdir(CSV_DIR):
    os.makedirs(CSV_DIR)


class MessageQueue:
    
    def __init__(self):
        self.file_path = f'{CSV_DIR}/{FILE_NAME}.csv'
        print(self.file_path)
        if path.exists(self.file_path):
            self.df = pd.read_csv(self.file_path, index_col=0)
            self.df.index = pd.to_datetime(self.df.index)
        else:
            self.df = pd.DataFrame(columns=['message_id', 'channel_id'])

    def __del__(self):
        print(self.file_path)
        self.df.to_csv(self.file_path)

    def add(self, message_id, channel_id):
        now = pd.to_datetime(datetime.now())
        self.df.loc[now] = [message_id, channel_id]
    
    def show(self):
        print(self.df)

