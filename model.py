import os
import csv
from pathlib import Path 
import math
import random
import time
import pandas
import numpy
import statistics

def player_edit(player):
	#given player string returns string without additional info
	place = 0
	for index,letter in enumerate(player):
		if letter == "\\":
			place = index
	return player[0:place]


def simulate_game(home_team,away_team,elos):
	#simulates a single game based on simple elo and updates elos
	home_elo = elos[home_team]
	away_elo = elos[away_team]
	#home_field_advantage in bball is ? I"m guessing its worth a solid 20 elo in covid-19 times
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

def generate_team_bpm_adj(team,rosters,stats):
	#given player stats and rosters we attempt to calculate an estimated ELO score for the season
	roster = rosters.loc[team]["Player"]
	players = {}
	for player in roster:
		players[player] = 0
	team_BPM_adj = 0
	#advanced stats found in stats[1]
	for player in stats[1].index:
		if player in players:
			bpm = stats[1].loc[player]["BPM"]
			mins = stats[1].loc[player]["MP"]
			games = stats[1].loc[player]["G"]
			if mins < 200:
				pass
			else:
				mins_g = round(mins/games/48,3)
				bpm_adj = bpm*mins_g
				players[player] = bpm_adj
	#advanced stats found in stats[0]
	for player in stats[0].index:
		if player in players:
			bpm = stats[0].loc[player]["BPM"]
			mins = stats[0].loc[player]["MP"]
			games = stats[0].loc[player]["G"]
			if mins < 150:
				pass
			else:
				mins_g = round(mins/games/48,3)
				bpm_adj = bpm*mins_g
				players[player] = (players[player]*2 + bpm_adj)/3
	
	exp = rosters.loc[team].at[team,"Exp"]
	for index,player in enumerate(players):
		if exp[index] == "R":
			pass
		else:
			if int(exp[index]) < 5:
				growth = random.uniform(1.0,1.16)
				if players[player] > 0:
					players[player] = players[player]*growth
				else:
					players[player] = players[player]/growth
			elif int(exp[index]) > 13:
				growth = random.uniform(0.84,1.0)
				if players[player] > 0:
					players[player] = players[player]*growth
				else:
					players[player] = players[player]/growth

	for player in players:
		team_BPM_adj += players[player]
	team_BPM_adj = round(team_BPM_adj/5,3)
	return team_BPM_adj

def generate_elos(teams_BPM_adj):
	#generates elos from a list of adj team bpm
	bpms = []
	elos = {}
	for team in teams_BPM_adj:
		bpms.append(teams_BPM_adj[team])
		elos[team] = 0
	mean = sum(bpms)/len(bpms)
	std_dev = statistics.pstdev(bpms)
	new_mean = 1500
	new_std = 100
	for team in elos:
		elos[team] = round(new_mean+(teams_BPM_adj[team]-mean)*(new_std/std_dev),1)
	return(elos)




#season has 72 games and now we set up the matchups with no regard to schedule or home vs away
#each team plays 3 intraconference games and 2 interconference games (14*3+2*15) = 72
def simulate_season(eastern_conference,western_conference,elos,records,schedule,stats):
	#main model which simulates a season with the option of giving a schedule
	games_played = []
	for row in schedule.index:
		home_team = schedule.loc[row]["Home Team"]
		away_team = schedule.loc[row]["Away Team"]
		result = simulate_game(home_team,away_team,elos)
		game = [home_team,away_team,result]
		games_played.append(game)
		if result == 1:
			records[home_team][0] +=1
			records[away_team][1] +=1
		else:
			records[home_team][1] +=1
			records[away_team][0] +=1
	return records

if __name__ == "__main__":
	# Here we run the code to simulate n number of seasons and find a mean win/loss count for the teams
	start = time.time()
	#list out data files in data folder and save them to new variable names for easy access
	data_files = []
	entries = Path("C:/Users/SEDan/Documents/github/NBA-predictor/data/")
	for entry in entries.iterdir():
		file = "C:/Users/SEDan/Documents/github/NBA-predictor/data/" + entry.name
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
	team_per_game.set_index("Team",inplace=True)
	team_total.set_index("Team",inplace=True)
	team_rosters.set_index("Team",inplace=True)
	advanced_stats_2020.loc[:,"Player"] = advanced_stats_2020.loc[:,"Player"].apply(player_edit)
	advanced_stats_2019.loc[:,"Player"] = advanced_stats_2019.loc[:,"Player"].apply(player_edit)
	per_game_stats_2019.loc[:,"Player"] = per_game_stats_2019.loc[:,"Player"].apply(player_edit)
	per_game_stats_2020.loc[:,"Player"] = per_game_stats_2020.loc[:,"Player"].apply(player_edit)
	advanced_stats_2019.set_index("Player",inplace=True)
	advanced_stats_2020.set_index("Player",inplace=True)
	per_game_stats_2019.set_index("Player",inplace=True)
	per_game_stats_2020.set_index("Player",inplace=True)

	stats = [advanced_stats_2019,advanced_stats_2020,per_game_stats_2019,per_game_stats_2020,team_per_game,team_total,team_rosters]

	#list of teams and lists of each conference
	teams = []
	for team in team_per_game.index:
		if team in teams:
			pass
		else:
			teams.append(team)
	# teams = ["Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets", "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets", "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers", "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat", "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks", "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns", "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors", "Utah Jazz", "Washington Wizards"]
	eastern_conference = ["Atlanta Hawks","Boston Celtics","Brooklyn Nets","Charlotte Hornets","Chicago Bulls","Cleveland Cavaliers","Detroit Pistons","Indiana Pacers","Miami Heat","Milwaukee Bucks","New York Knicks","Orlando Magic","Philadelphia 76ers","Toronto Raptors","Washington Wizards"]
	western_conference = []
	for team in teams:
		if team not in eastern_conference:
			western_conference.append(team)

	total_records = {"Atlanta Hawks": [0, 0], "Boston Celtics": [0, 0], "Brooklyn Nets": [0, 0], "Charlotte Hornets": [0, 0], "Chicago Bulls": [0, 0], "Cleveland Cavaliers": [0, 0], "Dallas Mavericks": [0, 0], "Denver Nuggets": [0, 0], "Detroit Pistons": [0, 0], "Golden State Warriors": [0, 0], "Houston Rockets": [0, 0], "Indiana Pacers": [0, 0], "Los Angeles Clippers": [0, 0], "Los Angeles Lakers": [0, 0], "Memphis Grizzlies": [0, 0], "Miami Heat": [0, 0], "Milwaukee Bucks": [0, 0], "Minnesota Timberwolves": [0, 0], "New Orleans Pelicans": [0, 0], "New York Knicks": [0, 0], "Oklahoma City Thunder": [0, 0], "Orlando Magic": [0, 0], "Philadelphia 76ers": [0, 0], "Phoenix Suns": [0, 0], "Portland Trail Blazers": [0, 0], "Sacramento Kings": [0, 0], "San Antonio Spurs": [0, 0], "Toronto Raptors": [0, 0], "Utah Jazz": [0, 0], "Washington Wizards": [0, 0]}
	teams_BPM_adj = {}
	n = 10
	for i in range(n):
		#player based elo on december 17 2020 (before season started) based on 538
		for team in teams:
			teams_BPM_adj[team] = generate_team_bpm_adj(team,team_rosters,stats)
		elos = generate_elos(teams_BPM_adj)
		records = {"Atlanta Hawks": [0, 0], "Boston Celtics": [0, 0], "Brooklyn Nets": [0, 0], "Charlotte Hornets": [0, 0], "Chicago Bulls": [0, 0], "Cleveland Cavaliers": [0, 0], "Dallas Mavericks": [0, 0], "Denver Nuggets": [0, 0], "Detroit Pistons": [0, 0], "Golden State Warriors": [0, 0], "Houston Rockets": [0, 0], "Indiana Pacers": [0, 0], "Los Angeles Clippers": [0, 0], "Los Angeles Lakers": [0, 0], "Memphis Grizzlies": [0, 0], "Miami Heat": [0, 0], "Milwaukee Bucks": [0, 0], "Minnesota Timberwolves": [0, 0], "New Orleans Pelicans": [0, 0], "New York Knicks": [0, 0], "Oklahoma City Thunder": [0, 0], "Orlando Magic": [0, 0], "Philadelphia 76ers": [0, 0], "Phoenix Suns": [0, 0], "Portland Trail Blazers": [0, 0], "Sacramento Kings": [0, 0], "San Antonio Spurs": [0, 0], "Toronto Raptors": [0, 0], "Utah Jazz": [0, 0], "Washington Wizards": [0, 0]}
		new_records = simulate_season(eastern_conference,western_conference,elos,records,schedule,stats)
		for record in new_records:
			total_records[record][0] += new_records[record][0]
			total_records[record][1] += new_records[record][1]
	for record in total_records:
		total_records[record][0] = round(total_records[record][0]/n,1)
		total_records[record][1] = round(total_records[record][1]/n,1)
	for record in total_records:
		print(record,total_records[record])
	end = time.time()
	print("this program took a total of ",round(end-start,2),"seconds to run for an n of ",n)



#defunct data goes below this line and is commented out
# elos = {"Atlanta Hawks": 1536, "Boston Celtics": 1602, "Brooklyn Nets": 1578, "Charlotte Hornets": 1396, "Chicago Bulls": 1421, "Cleveland Cavaliers": 1380, "Dallas Mavericks": 1584, "Denver Nuggets": 1613, "Detroit Pistons": 1354, "Golden State Warriors": 1488, "Houston Rockets": 1607, "Indiana Pacers": 1537, "Los Angeles Clippers": 1637, "Los Angeles Lakers": 1658, "Memphis Grizzlies": 1515, "Miami Heat": 1594, "Milwaukee Bucks": 1632, "Minnesota Timberwolves": 1483, "New Orleans Pelicans": 1552, "New York Knicks": 1382, "Oklahoma City Thunder": 1466, "Orlando Magic": 1512, "Philadelphia 76ers": 1603, "Phoenix Suns": 1604, "Portland Trail Blazers": 1559, "Sacramento Kings": 1503, "San Antonio Spurs": 1495, "Toronto Raptors": 1607, "Utah Jazz": 1590, "Washington Wizards": 1430}
# elos_list = list(elos.values())
# mean = sum(elos_list)/len(elos_list)
# std_dev = statistics.pstdev(elos_list)
# new_elos = {}
# for elo in elos:
# 	new_elos[elo] = round(1500+(elos[elo]-mean)*(100/std_dev),1)
# elos1 = generate_elos(teams_BPM_adj)
# for elo in new_elos:
# 	#comparision of 538 elos and my elos
# 	print(elo,elos1[elo],new_elos[elo])