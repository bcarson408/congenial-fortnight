from bs4 import BeautifulSoup
import requests
# import pymysql.cursors
import lxml
import re
import time
import pdb



base_url ="https://www.cbssports.com/fantasy/football/stats/posvsdef/"
positions = ["QB","RB","WR","TE","DST"]
stat_type = ["standard","advanced"]
qb_standard_stats = ['Att', 'Cmp', 'Yd', 'TD', 'Int', 'Rate', 'Att', 'Yd', 'Avg', 'TD', 'FL', 'FPTS']
team_dict = {}
players=[]
teams = []
players_dict = {}
team_dict = {}
season = range(1,3)
lines = []
dicts = ()
temp_list = []
counter = 0

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

def table_rows(table):
	print("function table_rows(table)")
	if len(table) == 1:
		for row in table[0].findAll('tr'):
			line=[]
			for cell in row.findAll('td'):
				line.append(cell.string)	
			if line not in lines:
# 				print line
				lines.append(line)
	return lines
	
	
	
def debug():
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "currentline player",line
	print
	print("Player List1:",id(players),players)
	print
	print
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
	
def debug2():
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "currentline player",line
	print
	print("Player List1:",id(players),players)
	print
	print
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++"



def createPlayerDict(line):
	# debug()
	print("createPlayerDict(line)",line)
	playersObjTracker(players)
	
	first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')
# 	print("first_element",first_element)
	first_element_length = len(first_element)
	if 	len(first_element) == 4:
		print("RAnk")
# 		print(str(line[:1])[3:-2],len(str(line[:1])))
		stat_headers = str(line[2:-1]).strip("u")
		players_dict['stat_headers_standard'] = stat_headers
		playersObjTracker(players)
	if len(first_element) == 0:
		player = line[1:2]
		player_stat = line[2:-1]
		players_dict['player_name']=player
		players_dict['player_stat']=player_stat
		print(">>>>>>> ",id(players_dict))
		
		playersObjTracker(players)
	
	# debug2()
		
def current_week(line):
	
	week_line = str(line).strip("[u'']")
	strlength = len(week_line)
	posOfweek = week_line.find("Week")
	thisWeek = week_line[posOfweek+5:]
	# print(thisWeek,len(thisWeek))
	team_dict['week'] = thisWeek
	players_dict['week'] = thisWeek
	position = week_line[:posOfweek-2]
# 		print(position,len(position))
	players_dict['position'] = position
# 	players.append(players_dict)
	playersObjTracker(players)

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
# 	print(team_dict)
# 	team_dict['week'] = players_dict['week']
	# print(team_dict)
# 	print(players_dict)
	
# 	if 	len(first_element) == 4:
# 		print("RAnk")
# # 		print(str(line[:1])[3:-2],len(str(line[:1])))
# 		stat_headers = str(line[2:-1]).strip("u")
# 		players_dict['stat_headers_standard'] = stat_headers
# 		print(players_dict)
# 	if len(first_element) == 0:
# 		player = line[1:2]
# 		player_stat = line[2:-1]
# 		players_dict['player_name']=player
# 		players_dict['player_stat']=player_stat
# 		print(players_dict)
# 	if len(line) == 14:
# 			matchupStr=str(line[1:2]).strip("[u'").rstrip(" [+]'").replace('\\xa0','')
# 			if 'Rank' in line[:1]:
# 	# 			print(str(line[:1])[3:-2],len(str(line[:1])))
# 				stat_headers = str(line[2:-1]).strip("u")
# 				players_dict['stat_headers_standard'] = stat_headers
# 				
# 	# 			print(stat_headers)
# 	# 			print(str(stat_headers).strip("[u''']"))
# 				# re.search()
# 			elif "vs" not in matchupStr :
# 				player = line[1:2]
# 				player_stat = line[2:-1]
# 				players_dict['player_name']=player
# 				players_dict['player_stat']=player_stat
# 	# 			print(players_dict)	
# 			if first_element.isdigit():
# 	# 			print("Game")			
# 				vs_pos = matchupStr.find("vs")
# 				opp_team = matchupStr[:vs_pos-4]
# 				team_mascot = matchupStr[vs_pos+3:-1]
# 	# 			print("Matchup :",matchupStr)
# 				vs_pos = matchupStr.find("vs")
# 				opp_team = matchupStr[:vs_pos-4]
# 				# print('opp_team',opp_team)
# 				team_mascot = matchupStr[vs_pos+3:-1]
# 	# 			print(team_mascot)
# 				team_dict['team_mascot'] = team_mascot
# 				players_dict['team'] = opp_team
# 				def_stats = str(line[2:-1])
# 				# print(team_dict)
# # 				print(players_dict)
# 	# 			print(def_stats.replace("[]",''))
# 	# 			print("This Weeks Def Stats",line[2:-1])
# 				team_dict['week_stats'] = line[2:-1]
# 				# print(team_dict)
# 				team_dict['week'] = players_dict['week']
# 				# print(team_dict)
# # 				print(players_dict)



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
	print "Player",players
	print "id",id(players_dict)
	if len(players) == 0:
		
		print "Players object is empty"
		print
	else:
		print "Players object has "+str(len(players))+" members:"
		for x in players:
			print(x,id(x),"\n")
		print
		

def main():
		counter = 0
# 		temp = base_url+pos
		type = str(stat_type[0:1]).strip("['']")
# 		fullUrl=base_url+pos+"/all/"+str(week)+"/"+type
		testUrl ="https://www.cbssports.com/fantasy/football/stats/posvsdef/QB/all/1/standard"
		my_soup = returnSoup(testUrl)
		mytext = my_soup.get_text(strip=True)
		doc_table = my_soup.findAll("table")
		table_rows(doc_table)
		print
		print
		playersObjTracker(players)
		print
		print
		pdb.set_trace()
		for l in lines:	
			counter += 1
			print 
			print
			print "Beging Loop",counter 
			print "currentline",l
			print "players_dict",id(players_dict),players_dict
			playersObjTracker(players)
			print
			
# 			print("Player List1:",players)
# 			print("LINE BEGIN")
			print len(l),len(str(l[:1])),l
			if len(l) == 14 and len(str(l[:1])) == 9:
				print
				print
				createPlayerDict(l)
			if len(l) == 14 and len(str(l[:1])) <= 8:
				print
				print
				createTeamDict(l)
			if len(l) == 1:
				print
				print
				current_week(l)
			print
			print "\nline :",l,"\nplayers_dict ",players_dict
			print "END Loop"
# 			pdb.set_trace()
			players.append(players_dict)
			
			time.sleep(3)
		
		playersObjTracker(players)
			
		time.sleep(3)
		# 
# 			players.append(players_dict)
# 			print
# 			print("Player List end:",players)
			# dicts = createDict(l)
# 			print dicts
		# print len(dicts),dicts
		# for x in dicts:
# 				print  "###################"
# 				print ">>>>> ",x
# 				time.sleep(2)
# 				print  "###################"
# 				if len(x) == 6:
# 					if x not in players:
# 						print "true"
# 					# 	players.append(x)
# # 						
# 						print ">>>>>>>>",len(players)
# 						time.sleep(3)
# 					else:
# 						pass
			
	
		
			# 
# 			else: 
# 				print 'false'
# 				players.append(dicts[:1])
			# if dicts[1:2] not in teams:
# 				print(str(dicts[1:2]))
# 				teams.append(dicts[1:2])
# 			






		    	
			
			


main()