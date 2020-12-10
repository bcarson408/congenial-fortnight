# from urllib import urlopen
from bs4 import BeautifulSoup
import requests
# import pymysql.cursors
import lxml
import re
import time
import pymysql
import pandas as pd
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
pos = ""
defense = []


def make_db_connection(): 
	connection = pymysql.connect(
							 host='localhost',
                             user='root',
                             password='ganja420',
                             db='testdb',
                             charset='utf8mb4',
        					 cursorclass=pymysql.cursors.DictCursor
        					 )
	return connection
	
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
		
		# print "players_dict :", players_dict
# 		print "temp_list :", temp_list
		temp_list.append( players_dict)
		time.sleep(3)
		# print "temp_list :", temp_list
# 		print(len(players_dict),players_dict)
# 		time.sleep(3)
# 		print  "###################"
	else:
		print("temp_list",temp_list)

# 	print
# 	print
# 	print("createDict(line) END")
	return(players_dict,team_dict)	
	
def printLines(line):
	print(line,"\n")
	
def passingStats(line):
	passing_stats = []
	for stat in stat_headers_str[2:8]:
		new_key = "passing_"+stat.lower()
		passing_stats.append(new_key)
	passing_stats_dict = dict(zip(passing_stats,map(float,line[2:8])))
	return passing_stats_dict
	
def qb_rushingStats(line):
	rushing_stats = []
	for stat in stat_headers_str[8:13]:
		new_key = "rushing_"+stat.lower()
		rushing_stats.append(new_key)
	rushing_stats_dict = dict(zip(rushing_stats,map(float,line[8:13])))
	return rushing_stats_dict
	
def rushingStats(line):
	rushing_stats = []
	for stat in stat_headers_str[2:6]:
		new_key = "rushing_"+stat.lower()
		rushing_stats.append(new_key)
	rushing_stats_dict = dict(zip(rushing_stats,map(float,line[2:6])))
	return rushing_stats_dict

def receivingStats(line):
	receiving_stats = []
	for stat in stat_headers_str[6:12]:
		new_key = "receiving_"+stat.lower()
		receiving_stats.append(new_key)
	receiving_stats_dict = dict(zip(receiving_stats,map(float,line[6:12])))
	return receiving_stats_dict
	
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
					line = line[1:3]
					print(line)
				if len(line) == 14:
					createPlayerDict(line)
				if len(line) == 13:
					marker = line[:1]
					if 'Rank' in line:
						lineStr = str(line).strip("[]")
						global stat_headers
						global stat_headers_str
						global rushing_stats_header
						global receiving_stats_headers 
						global fpts_stat
						stat_headers_str = line
						rushing_stats_headers = line[2:8]
						receiving_stats_headers = line[8:12]
						fpts_stat = line[-1]
					if marker[0].isdigit() == True:
						global team_dict
						matchup = str(line[1:2])
						matchup = matchup.strip("['']").strip("u'").replace('\\xa0','').rstrip(" [+")
						if str(matchup).find(pos)>0:
							player_pos = str(matchup).find(pos)
							home_team = matchup[str(matchup).find("vs")+3:]
							opp_team = matchup[:player_pos-1]
							matchup_stat = line[2:]
							team_dict = dict(zip(stat_headers_str[2:],map(float,line[2:])))
							team_dict["home"] = home_team 
							team_dict["opponent"] = opp_team
							team_dict["week"] = int(game_week_dict['week'][5:])
							team_dict["matchup"] = game_week_dict['positions'][:-1]
							print("Week "+game_week_dict['week'][5:]+": "+game_week_dict['positions'][:-1]+" matchup")
							print("x"*72)
							print(team_dict['home'])
							print(team_dict['opponent'])
							print(stat_headers_str[2:])
							print(matchup_stat)
							print("x"*72)
							print()
						
							
		
							teams.append(team_dict)
					if marker[0].isdigit() == False and 'Rank' not in line:
						passing_stats =[]
						player = str(line[1:2]).strip('"[u]"')
						player_stats = line[2:1]
						player_dict["fname"] = player[player.find(',')+2:-1]
						player_dict["lname"] = player[1:player.find(',')]
						player_dict['team'] = team_dict["opponent"] 
						rushingStats(line)
						receivingStats(line)
						player_dict.update(receivingStats(line))
						player_dict.update(rushingStats(line))
						player_dict["ftps"] = float(line[-1])
						player_dict['week'] = int(game_week_dict['week'][5:])
						player_dict['position']= game_week_dict['positions'][:-1]
						players.append(player_dict)
						player_dict = {}
										
def createPlayerDict(line):
	global player_dict
# 	print("createPlayerDict(line)",line,player_dict_id,player_dict)
	first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')
# 	print("first_element",first_element)
	first_element_length = len(first_element)
	marker = line[:1]
	if 'Rank' in line:
		lineStr = str(line).strip("[]")
		global stat_headers_str
		global passing_stats_header
		global rushing_stats_headers 
		global fpts_stat
		stat_headers_str = line
		passing_stats_headers = line[2:8]
		rushing_stats_headers = line[8:13]
		fpts_stat = line[-1]
	if marker[0].isdigit() == True:
		global team_dict
		matchup = str(line[1:2])
		matchup = matchup.strip("['']").strip("u'").replace('\\xa0','').rstrip(" [+")
		if str(matchup).find("QB")>0:
			player_pos = str(matchup).find("QB")
			home_team = matchup[str(matchup).find("vs")+3:]
			opp_team = matchup[:player_pos-1]
			matchup_stat = line[2:]
			team_dict = dict(zip(stat_headers_str[2:],map(float,line[2:])))
			team_dict["home"] = home_team 
			team_dict["opponent"] = opp_team
			team_dict["week"] = int(game_week_dict['week'][5:])
			team_dict["matchup"] = game_week_dict['positions'][:-1]
			print("Week "+game_week_dict['week'][5:]+": "+game_week_dict['positions'][:-1]+" matchup")
			print("x"*72)
			print(team_dict['home'])
			print(team_dict['opponent'])
			print(stat_headers_str[2:])
			print(matchup_stat)
			print("x"*72)
			print()
			teams.append(team_dict)
		else:
			player_pos = str(matchup).find("DST")
			home_team = matchup[str(matchup).find("vs")+3:]
			opp_team = matchup[:player_pos-1]
			matchup_stat = line[2:]
			team_dict = dict(zip(stat_headers_str[2:],map(float,line[2:]))) 
			team_dict['def_int'] = team_dict.pop("Int")
			team_dict["home"] = home_team 
			team_dict["opponent"] = opp_team
			team_dict["week"] = int(game_week_dict['week'][5:])
			team_dict["position"] = game_week_dict['positions'][:-1]
			print("Week "+game_week_dict['week'][5:]+": "+game_week_dict['positions'][:-1]+" matchup")
			print("x"*72)
			print(team_dict['home'])
			print(team_dict['opponent'])
			print(stat_headers_str[2:])
			print(matchup_stat)
			print("x"*72)
			print()
			defense.append(team_dict)
	if marker[0].isdigit() == False and 'Rank' not in line:
		player = str(line[1:2]).strip('"[u]"')
		player_stats = line[2:1]
		player_dict["fname"] = player[player.find(',')+2:-1]
		player_dict["lname"] = player[1:player.find(',')]
		player_dict['team'] = team_dict["opponent"]  
		passingStats(line)
		qb_rushingStats(line)
		player_dict.update(passingStats(line))
		player_dict.update(qb_rushingStats(line))
		player_dict['ftps'] = float(line[-1])
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
	print(len(first_element),line)
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


		
# for pos in positions:
# 	temp = base_url+pos
# 	a_type = str(stat_type[0:1]).strip("['']")
# 	for week in range(1,18):
# 		fullUrl=base_url+pos+"/all/"+str(week)+"/"+a_type
# 		my_soup = returnSoup(fullUrl)
# 		mytext = my_soup.get_text(strip=True)
# 		doc_table = my_soup.findAll("table")
# 		table_rows(doc_table)


drop_existing_qb_table = "drop table if exists quarterbacks" 
drop_existing_rb_table = "drop table if exists runningbacks" 
drop_existing_wr_table = "drop table if exists receivers"
drop_existing_matchup_table = "drop table if exists matchup"
drop_existing_def_table = "drop table if exists defense"

select_all = "select * from quarterbacks" 

create_qb_table = """ CREATE TABLE `quarterbacks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `team` VARCHAR(45) NULL,
  `passing_att` FLOAT NULL,
  `passing_cmp` FLOAT NULL,
  `passing_yd` FLOAT NULL,
  `passing_td` FLOAT NULL,
  `passing_int` FLOAT NULL,
  `passing_rate` FLOAT NULL,
  `rushing_att` FLOAT NULL,
  `rushing_yd` FLOAT NULL,
  `rushing_avg` FLOAT NULL,
  `rushing_td` FLOAT NULL,
  `rushing_fl` FLOAT NULL,
  `ftps` FLOAT NULL,
  `week` INT NULL,
  `position` VARCHAR(45) NULL,
  PRIMARY KEY (`id`)); """ 
  
create_rb_table = """ CREATE TABLE `runningbacks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `team` VARCHAR(45) NULL,
  `receiving_targt` FLOAT NULL,
  `receiving_recpt` FLOAT NULL,
  `receiving_yd` FLOAT NULL,
  `receiving_avg` FLOAT NULL,
  `receiving_td` FLOAT NULL,
  `receiving_fl` FLOAT NULL,
  `rushing_att` FLOAT NULL,
  `rushing_yd` FLOAT NULL,
  `rushing_avg` FLOAT NULL,
  `rushing_td` FLOAT NULL,
  `ftps` FLOAT NULL,
  `week` INT NULL,
  `position` VARCHAR(50) NULL,
  PRIMARY KEY (`id`));""" 
  
create_wr_table = """ CREATE TABLE `receivers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fname` VARCHAR(45) NULL,
  `lname` VARCHAR(45) NULL,
  `team` VARCHAR(45) NULL,
  `receiving_targt` FLOAT NULL,
  `receiving_recpt` FLOAT NULL,
  `receiving_yd` FLOAT NULL,
  `receiving_avg` FLOAT NULL,
  `receiving_td` FLOAT NULL,
  `receiving_fl` FLOAT NULL,
  `rushing_att` FLOAT NULL,
  `rushing_yd` FLOAT NULL,
  `rushing_avg` FLOAT NULL,
  `rushing_td` FLOAT NULL,
  `ftps` FLOAT NULL,
  `week` INT NULL,
  `position` VARCHAR(50) NULL,
  PRIMARY KEY (`id`));"""
  
create_teams_table =  """ CREATE TABLE IF NOT EXISTS `nfl_teams` (
  `team_id` INT NOT NULL AUTO_INCREMENT,
  `city` VARCHAR(45) NULL,
  `mascot` VARCHAR(45) NULL,
  `abv` VARCHAR(5) NULL,
  `abv1` VARCHAR(5) NULL,
  `division` VARCHAR(5) NULL,
  `conference` VARCHAR(25) NULL,
  PRIMARY KEY (`team_id`))
ENGINE = InnoDB
"""
create_def_table = """ CREATE TABLE `testdb`.`defense` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `def_int` FLOAT NULL,
  `STY` FLOAT NULL,
  `SACK` FLOAT NULL,
  `TK` FLOAT NULL,
  `DFR` FLOAT NULL,
  `FF` FLOAT NULL,
  `DTD` FLOAT NULL,
  `PA` FLOAT NULL,
  `PaNetA` FLOAT NULL,
  `RuYdA` FLOAT NULL,
  `TYdA` FLOAT NULL,
  `FPTS` FLOAT NULL,
  `home` VARCHAR(45) NULL,
  `opponent` VARCHAR(45) NULL,
  `week` INT NULL,
  `position` VARCHAR(50) NULL,
  PRIMARY KEY (`id`));
"""
create_matchup_table = """ CREATE TABLE `testdb`.`matchup` (
  `id` INT NOT NULL,
  `att` FLOAT NULL,
  `yd` FLOAT NULL,
  `avg` FLOAT NULL,
  `td` FLOAT NULL,
  `targt` FLOAT NULL,
  `recpt` FLOAT NULL,
  `fl` FLOAT NULL,
  `FPTS` FLOAT NULL,
  `home` VARCHAR(45) NULL,
  `opponent` VARCHAR(45) NULL,
  `week` INT NULL,
  PRIMARY KEY (`id`));
"""
 
def insertDataToTable(table,data_dict):
	placeholders = ', '.join(['%s'] * len(data_dict))
	columns = ', '.join(data_dict.keys())
	col_list = columns.split(",")
	values = tuple(data_dict.values())
# 	str(columns.split(",")).replace('\'','')
	sql = "insert into %s (%s) values %s;" %(table,str(columns.split(",")).strip("[]").replace('\'',''),values)
	return sql


def main():
	global pos
	con = make_db_connection()
	cur = con.cursor()
	for pos in positions:
# 		fullUrl=base_url+pos+"/all/"+str(week)+"/"+type
		for week in range(1,18):
			testUrl ="https://www.cbssports.com/fantasy/football/stats/posvsdef/"+pos+"/all/"+str(week)+"/standard"
			my_soup = returnSoup(testUrl)
			mytext = my_soup.get_text(strip=True)
			doc_table = my_soup.findAll("table")
			table_rows(doc_table)
	for dfense in defense:
		print(dfense)
		show_tables = "SHOW TABLES LIKE 'defense'"
		cur.execute(show_tables)
		result = cur.fetchone()
		if result:
			cur.execute(insertDataToTable('defense',dfense))
		else:
			cur.execute(create_def_table)
			result = cur.execute(insertDataToTable('defense',dfense))
			cur.fetchall()
		con.commit()
	for player in players:
		if player['position'] == 'Quarterback':
			print(player)
			with con:
				cur = con.cursor()
				show_tables = "SHOW TABLES LIKE 'quarterbacks'"
				cur.execute(show_tables)
				result = cur.fetchone()
				if result:
					cur.execute(insertDataToTable('quarterbacks',player))
				else:# there are no tables named "tableName"
					cur.execute(create_qb_table)
					result = cur.execute(insertDataToTable('quarterbacks',player))
					print(result)
				cur.fetchall()
			con.commit()
		if player['position'] == 'Running Back':
			print(player)
			with con:
				cur = con.cursor()
				show_tables = "SHOW TABLES LIKE 'runningbacks'"
				cur.execute(show_tables)
				result = cur.fetchone()
				if result:
					cur.execute(insertDataToTable('runningbacks',player))
				else:# there are no tables named "tableName"
					cur.execute(create_rb_table)
					result = cur.execute(insertDataToTable('runningbacks',player))
					print(result)
				cur.fetchall()
			con.commit()
		if player['position'] == 'Wide Receiver':
			print(player)
			with con:
				cur = con.cursor()
				show_tables = "SHOW TABLES LIKE 'receivers'"
				cur.execute(show_tables)
				result = cur.fetchone()
				if result:
					cur.execute(insertDataToTable('receivers',player))
				else:# there are no tables named "tableName"
					cur.execute(create_wr_table)
					result = cur.execute(insertDataToTable('receivers',player))
					print(result)
				cur.fetchall()
			con.commit()
	for team in teams:
		print(team)
		cur = con.cursor()
		show_tables = "SHOW TABLES LIKE 'quarterbacks'"
		cur.execute(show_tables)
		result = cur.fetchone()
		if result:
			cur.execute(insertDataToTable('quarterbacks',player))
		else:# there are no tables named "tableName"
			cur.execute(create_qb_table)
			result = cur.execute(insertDataToTable('quarterbacks',player))
			print(result)
		cur.fetchall()
	con.commit()
	for df in defense:
		print(df,end="\n\n")
		
	df = pd.DataFrame(players)
	print(df)
	






		    	
			
			


main()