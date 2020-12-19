import os
import csv
from pathlib import Path 
import math
import random
import time
import pandas
import numpy


#list out data files in data folder and save them to new variable names for easy access
data_files = []
entries = Path('C:/Users/SEDan/Documents/github/NBA-predictor/data/')
for entry in entries.iterdir():
	file = 'C:/Users/SEDan/Documents/github/NBA-predictor/data/' + entry.name
	data_files.append(file)

advanced_stats = pandas.read_csv(data_files[0])
per_game_stats = pandas.read_csv(data_files[1])
team_per_game = pandas.read_csv(data_files[2])
team_total = pandas.read_csv(data_files[3])
team_per_game.set_index('Team',inplace=True)
team_total.set_index('Team',inplace = True)
advanced_stats.set_index('Player',inplace=True)
per_game_stats.set_index('Player',inplace=True)

#dictionary of teams where each key is a team and each value is a list of roster players updated on 12/19/20
team_rosters = {}
for team in team_per_game.index:
	team_rosters[team] = []
print(team_rosters)
print(advanced_stats)
print(per_game_stats)
print(team_total)
print(team_per_game)
