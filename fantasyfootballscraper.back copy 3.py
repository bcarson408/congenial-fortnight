from bs4 import BeautifulSoup
import requests

import lxml
import re
import time
import pdb;pdb.set_trace()



base_url ="https://www.cbssports.com/fantasy/football/stats/posvsdef/"
positions = ["QB","RB","WR","TE","DST"]
stat_type = ["standard","advanced"]
qb_standard_stats = ['Att', 'Cmp', 'Yd', 'TD', 'Int', 'Rate', 'Att', 'Yd', 'Avg', 'TD', 'FL', 'FPTS']
team_dict = {}
players=[]
teams = []
player_dict = {}
player_dict_id = id(player_dict)
team_dict = {}
season = range(1,3)
lines = []
dicts = ()
temp_list = []
counter = 0
stat_headers_str = ""
stat_headers_list = []
player_position	 = ""
game_week = ""
team_dict = { }
game_week_dict = {}
passing_stat_headers = []
rushing_stat_headers =[]
fantasy_points = ""


def returnSoup(url):
	response = requests.get(url)
	page = response.content
	return BeautifulSoup(page,'html.parser')	
	
def strip_line(line):
	print("Line",line)
	lines.append(line)
	return lines
		
def createDict(line):
	print("createDict(line) BEGIN")
	thisWeek_dict ={}
	week_of_season = 0
	thisWeek = 0
	first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')
	# print(first_element,len(first_element))
	first_element_length = len(first_element)
	if len(line)==1:
			current_week_line = str(line).strip("[u'']")
			strlength = len(current_week_line)
			posOfweek = current_week_line.find("Week")
			thisWeek = current_week_line[posOfweek+5:]
			players_dict['week'] = thisWeek
			position = current_week_line[:posOfweek-2]

			players_dict['position'] = position	
	if len(line) == 4:
			pass
	if players_dict not in temp_list:
		temp_list.append( players_dict)
		time.sleep(3)
		print(len(players_dict),players_dict)
		time.sleep(3)
	else:
		print("temp_list",temp_list)
	return(players_dict,team_dict)	
	
def table_rows(table):
	if len(table) == 1:
		for row in table[0].findAll('tr'):
			player_dict = {}
			line=[]
			for cell in row.findAll('td'):
				line.append(cell.string)	
			if line not in lines:

				if len(line) == 1:
					 current_week(line)
				if len(line) == 4:
					print(line)
				if len(line) == 14:
					createPlayerDict(line)

def passing_stat(stats):
	prefixStr = "passing_"	
	for key in stats.keys():
		newKey = prefixStr+key
		stats[newKey] = stats.pop(key)
	return stats

def rushing_stat(stats):
	prefixStr = "passing_"	
	for key in stats.keys():
		newKey = prefixStr+key
		stats[newKey] = stats.pop(key)
	return stats
		
def createPlayerDict(line):
	global player_dict
	first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')
	first_element_length = len(first_element)
	marker = line[:1]
	if 'Rank' in line:
		global stat_headers_list 
		global passing_stat_headers
		global rushing_stats_header
		global fantasy_points 
		stat_headers_list = list(map(str.lower,line[2:]))
		passing_stat_headers = stat_headers_list[:6]
		rushing_stat_headers = stat_headers_list[7:] 
		fantasy_points = stat_headers_list[-1]
	if marker[0].isdigit() == True:
		print("Matchup:")
		matchup = str(line[1:2])
		matchup = matchup.strip("['']").strip("u'").replace('\\xa0','').rstrip(" [+")
		player_pos = str(matchup).find("QB")
		home_team = matchup[str(matchup).find("vs")+3:]
		opp_team = matchup[:player_pos-1]
		matchup_stat = line[2:]
		global team_dict
		team_dict["home"] = home_team 
		team_dict["opponent"] = opp_team

	if marker[0].isdigit() == False and 'Rank' not in line:
		player = str(line[1:2]).strip('"[u]"')
		player_stats = line[2:1]
		player_dict["fname"] = player[player.find(',')+2:-1]
		player_dict["lname"] = player[1:player.find(',')]
		player_dict['team'] = team_dict["opponent"]  
		passing_headers = ['passing_att','passing_cmp','passing_yd','passing_td','passing_int','passing_rate']
		rushing_headers = ['rsushing_att','rushing_yd','rushing_avg','rushing_td','fumbles_lost']

		passing_stats = dict(zip(passing_headers,line[2:8]))
		rushing_stats = dict(zip(rushing_headers,line[8:13]))			
		player_dict.update(passing_stats)
		player_dict.update(rushing_stats)
		player_dict['ftps'] = line[-1]
		player_dict['week'] = int(game_week_dict['week'][5:])
		player_dict['position']= game_week_dict['positions'][:-1]
		players.append(player_dict)
		player_dict = {}
				
def current_week(line):
	week_line = str(line).strip("[u'']")
	week_posistion = week_line.find('Week')
	player_position = week_line[:week_line.find('Week')-1]
	game_week = week_line[week_line.find('Week'):]
	game_week_dict['week'] =  game_week
	game_week_dict['positions'] = player_position
	return game_week_dict
	
def createTeamDict(line):
	print("createPlayerDict(line)",line)
	first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')

	first_element_length = len(first_element)
	matchupStr=str(line[1:2]).strip("[u'").rstrip(" [+]'").replace('\\xa0','')
	vs_pos = matchupStr.find("vs")
	opp_team = matchupStr[:vs_pos-4]
	team_mascot = matchupStr[vs_pos+3:-1]
	print("Matchup :",matchupStr)
	vs_pos = matchupStr.find("vs")
	opp_team = matchupStr[:vs_pos-4]
	# print('opp_team',opp_team)
	team_mascot = matchupStr[vs_pos+3:-1]

	team_dict['team_mascot'] = team_mascot
	players_dict['team'] = opp_team
	def_stats = str(line[2:-1])
	print(def_stats.replace("[]",''))
	print("This Weeks Def Stats",line[2:-1])
	team_dict['week_stats'] = line[2:-1]




def backup():
	for pos in positions:
		temp = base_url+pos
		type = str(stat_type[0:1]).strip("['']")
		fullUrl=base_url+pos+"/all/"+str(week)+"/"+type
		testUrl ="https://www.cbssports.com/fantasy/football/stats/posvsdef/QB/all/1/standard"
		my_soup = returnSoup(testUrl)
		mytext = my_soup.get_text(strip=True)
		doc_table = my_soup.findAll("table")
		table_rows(doc_table)	

def insertFromDict(table, dict):
    """Take dictionary object dict and produce sql for 
    inserting it into the named table"""
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(dict)
    sql += ') VALUES ('
    sql += ', '.join(map(dictValuePad, dict))
    sql += ');'
    return sql
    

		

for pos in positions:
	temp = base_url+pos
	type = str(stat_type[0:1]).strip("['']")
	for week in range(1,18):
		fullUrl=base_url+pos+"/all/"+str(week)+"/"+type
		my_soup = returnSoup(fullUrl)
		mytext = my_soup.get_text(strip=True)
		doc_table = my_soup.findAll("table")
		table_rows(doc_table)


def main():
	for pos in positions:
		testUrl ="https://www.cbssports.com/fantasy/football/stats/posvsdef/"+pos+"/all/1/standard"
		my_soup = returnSoup(testUrl)
		mytext = my_soup.get_text(strip=True)
		doc_table = my_soup.findAll("table")
		table_rows(doc_table)
	for player in players:
		print(player,"\n")


	






		    	
			
			


main()