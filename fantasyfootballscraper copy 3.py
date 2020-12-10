from urllib import urlopen
from bs4 import BeautifulSoup
import requests
# import pymysql.cursors
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



def returnSoup(url):
	response = requests.get(url)
	page = response.content
	return BeautifulSoup(page,'html.parser')	
def strip_line(line):
	print("Line",line)
	lines.append(line)
# 	print(str(line),len(line))
# 	Quarterbacks Week 7
#   12345678901234567890
#            1         2
	
	return lines
	# return(players_dict,team_dict)	
def createDict(line):
	print("createDict(line) BEGIN")
	thisWeek_dict ={}
	week_of_season = 0
	thisWeek = 0
	first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')
	# print(first_element,len(first_element))
	first_element_length = len(first_element)
	if len(line)==1:
# 			print('current week')
			current_week_line = str(line).strip("[u'']")
# 			print(current_week_line)
			strlength = len(current_week_line)
			posOfweek = current_week_line.find("Week")
			thisWeek = current_week_line[posOfweek+5:]
			players_dict['week'] = thisWeek
			position = current_week_line[:posOfweek-2]
# 			print(position,len(position))
			players_dict['position'] = position	
	if len(line) == 4:
			pass
						
# 	print(team_dict)
	# print line
	if players_dict not in temp_list:
		print  "###################"
		print "players_dict :", players_dict
		print "temp_list :", temp_list
		temp_list.append( players_dict)
		time.sleep(3)
		print "temp_list :", temp_list
		print(len(players_dict),players_dict)
		time.sleep(3)
		print  "###################"
	else:
		print "temp_list",temp_list

# 	print
# 	print
# 	print("createDict(line) END")
	return(players_dict,team_dict)	
	
	
def printLines(line):
	print line,"\n"

def table_rows(table):
	if len(table) == 1:
		for row in table[0].findAll('tr'):
			player_dict = {}
			line=[]
			for cell in row.findAll('td'):
				line.append(cell.string)	
			if line not in lines:
# 				print line
				if len(line) == 1:
					 current_week(line)
				if len(line) == 4:
					print(line)
				if len(line) == 14:
					createPlayerDict(line)


	
	
	



def createPlayerDict(line):
	global player_dict
# 	print("createPlayerDict(line)",line,player_dict_id,player_dict)
	first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')
# 	print("first_element",first_element)
	first_element_length = len(first_element)
	marker = line[:1]
	if 'Rank' in line:
		lineStr = ','.join(line)
		lineStr.encode('ascii','ignore')
		global stat_headers_str
		stat_headers_str = lineStr.encode()
		global stat_headers_list 
		stat_headers_list = stat_headers_str.split()
	if marker[0].isdigit() == True:
		print("Matchup:")
		matchup = str(line[1:2])
		matchup = matchup.strip("['']").strip("u'").replace('\\xa0','').rstrip(" [+")
		player_pos = str(matchup).find("QB")
		home_team = matchup[str(matchup).find("vs")+3:]
		opp_team = matchup[:player_pos-1]
		matchup_stat = line[2:]
		global team_dict
		team_dict = dict(zip(stat_headers_str.split(",")[2:],line[2:]))
		team_dict["home"] = home_team 
		team_dict["opponent"] = opp_team
		teams.append(team_dict)
	if marker[0].isdigit() == False and 'Rank' not in line:
		# print(line)
# 		print(team_dict)
		player = str(line[1:2]).strip('"[u]"')
		player_stats = line[2:1]
		player_dict["fname"] = player[player.find(',')+2:-1]
		player_dict["lname"] = player[1:player.find(',')]
		player_dict['team'] = team_dict["opponent"]  
		player_dict.update(dict(zip(stat_headers_str.split(",")[2:],map(float,line[2:]))))
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
# 	print("first_element",first_element)
	first_element_length = len(first_element)
	print len(first_element),line
	matchupStr=str(line[1:2]).strip("[u'").rstrip(" [+]'").replace('\\xa0','')
	vs_pos = matchupStr.find("vs")
	opp_team = matchupStr[:vs_pos-4]
	team_mascot = matchupStr[vs_pos+3:-1]
	print("Matchup :",matchupStr)
	vs_pos = matchupStr.find("vs")
	opp_team = matchupStr[:vs_pos-4]
	# print('opp_team',opp_team)
	team_mascot = matchupStr[vs_pos+3:-1]
# 			print(team_mascot)
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
# 			print(my_soup.prettify())
		mytext = my_soup.get_text(strip=True)
# 			print(mytext)
		doc_table = my_soup.findAll("table")
		# print(doc_table)
		table_rows(doc_table)	

def playersObjTracker(players):
	print("id:", id(players))
	print
	print "Players",players,id(players)
	print "players_dict id",id(players_dict)
	if len(players) == 0:
		
		print "Players object is empty"
		print
	else:
		print "Players object has "+str(len(players))+" members:"
		for x in players:
			print(x,id(x),"\n")
		print
		

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
		fullUrl=base_url+pos+"/all/"+str(week)+"/"+type
		for week in range(1,18):
			testUrl ="https://www.cbssports.com/fantasy/football/stats/posvsdef/"+pos+"/all/"+str(week)+"/standard"+type
			my_soup = returnSoup(testUrl)
			mytext = my_soup.get_text(strip=True)
			doc_table = my_soup.findAll("table")
			table_rows(doc_table)
# 	for player in players:
# 		print(player,"\n")
# 	for team in teams:
# 		print(team,"\n")
	






		    	
			
			


main()