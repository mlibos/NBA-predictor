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

stats = [advanced_stats_2019,advanced_stats_2020,per_game_stats_2019,per_game_stats_2020,team_per_game,team_total,team_rosters]

#list of teams and lists of each conference
teams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']
eastern_conference = ['Atlanta Hawks','Boston Celtics','Brooklyn Nets','Charlotte Hornets','Chicago Bulls','Cleveland Cavaliers','Detroit Pistons','Indiana Pacers','Miami Heat','Milwaukee Bucks','New York Knicks','Orlando Magic','Philadelphia 76ers','Toronto Raptors','Washington Wizards']
western_conference = []
for team in teams:
	if team not in eastern_conference:
		western_conference.append(team)

#season has 72 games and now we set up the matchups with no regard to schedule or home vs away
#each team plays 3 intraconference games and 2 interconference games (14*3+2*15) = 72
def simulate_season(eastern_conference,western_conference,stats,schedule = None):
	#main model which simulates a season with the option of giving a schedule
	pass

def simulate_game(home_team,away_team,elos):
	#simulates a single game based on simple elo and updates elos
	home_elo = elos[home_team]
	away_elo = elos[away_team]
	#home_field_advantage in bball is ? I'm guessing its worth a solid 20 elo in covid-19 times
	home_elo += 20
	expected_home = 1/(1+10**((away_elo-home_elo)/400))
	expected_away = 1-expected_home
	event = random.random()
	result = 0
	#538 says a k factor of 20 is optimal for basketball
	k = 20
	if event > expected_home:
		result = 0
		elos[home_team] = round((elos[home_team] + k*(0-expected_home)),1)
		elos[away_team] = round((elos[away_team] + k*(1-expected_away)),1)
	elif event <= expected_home:
		result = 1
		elos[home_team] = round((elos[home_team] + k*(1-expected_home)),1)
		elos[away_team] = round((elos[away_team] + k*(0-expected_away)),1)
	return(result)
elos = {}
elos['ATL'] = 1550
elos['BOS'] = 1550
atl_wins = 0
for i in range(1):
	result = simulate_game('ATL','BOS',elos)
	if result == 1:
		atl_wins +=1
print(atl_wins,elos,)

	


