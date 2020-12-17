import os
import csv
from pathlib import Path 
import math
import random
import time
import pandas



data_files = []
#list out data files in data folder and save them to new variable names for easy access
entries = Path('C:/Users/SEDan/Documents/github/NBA-predictor/data/')
for entry in entries.iterdir():
	file = 'C:/Users/SEDan/Documents/github/NBA-predictor/data/' + entry.name
	data_files.append(file)

advanced_stats = pandas.read_csv(data_files[0])
per_game_stats = pandas.read_csv(data_files[1])
team_per_game = pandas.read_csv(data_files[2])
team_total = pandas.read_csv(data_files[3])

# print(advanced_stats,'\n',per_game_stats,'\n',team_per_game,'\n',team_total)
