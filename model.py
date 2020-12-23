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

#create dataframes and make them pretty
advanced_stats_2019 = pandas.read_csv(data_files[0])
advanced_stats_2020 = pandas.read_csv(data_files[1])
schedule = pandas.read_csv(data_files[2])
per_game_stats_2019 = pandas.read_csv(data_files[3])
per_game_stats_2020 = pandas.read_csv(data_files[4])
team_per_game = pandas.read_csv(data_files[5])
team_total = pandas.read_csv(data_files[6])
team_rosters = pandas.read_csv(data_files[7])
team_per_game.set_index('Team',inplace=True)
team_total.set_index('Team',inplace=True)
team_rosters.set_index('Team',inplace=True)
advanced_stats_2019.set_index('Player',inplace=True)
advanced_stats_2020.set_index('Player',inplace=True)
per_game_stats_2019.set_index('Player',inplace=True)
per_game_stats_2020.set_index('Player',inplace=True)
#list of teams
teams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']
#dictionary where keys are teams and values are number of games played in released schedule (approx half of the schedule)
teams_games = {}
for team in teams:
	teams_games[team] = 0
#checking released schedule
for game in schedule.index:
	home_team = schedule.loc[game]['Home Team']
	away_team = schedule.loc[game]['Away Team']
	teams_games[home_team] += 1
	teams_games[away_team] += 1
