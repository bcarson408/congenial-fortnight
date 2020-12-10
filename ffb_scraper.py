from urllib import urlopen
from bs4 import BeautifulSoup
import requests
# import pymysql.cursors
import lxml

base_url ="https://www.cbssports.com/fantasy/football/stats/posvsdef/"
positions = ["QB","RB","WR","TE","DST"]
stat_type = ["standard","advanced"]
qb_standard_stats = ['Att', 'Cmp', 'Yd', 'TD', 'Int', 'Rate', 'Att', 'Yd', 'Avg', 'TD', 'FL', 'FPTS']
players=[]
teams = []
players_dict = {}
team_dict = {}

week = 0
stat_headers = []
line_striped = ""
line=""
temp2 =""
stat_headers=""
teams = []

def returnSoup(url):
	response = requests.get(url)
	page = response.content
	return BeautifulSoup(page,'lxml')
	

def getThisWeek(line,thisWeek_dict):	
	if len(line)==1:
		week_of_season = str(line).strip("[u'']")
		strlength = len(week_of_season)
		posOfweek = week_of_season.find("Week")
		thisWeek = week_of_season[posOfweek+5:]
		thisWeek_dict['week'] = thisWeek
		position = week_of_season[:posOfweek]
		thisWeek_dict['position'] = position
	return thisWeek_dict
	
	
def playerList(line):
			players_dict = {}
			player_name = line[1:2]
			players_dict['name'] = str(player_name).strip("[u'']")
			players_dict['weekly_stats'] = str(line[2:-1])
			line =str(line).strip()
			return players_dict
			

def table_rows(table):
	team_dict = {}
	thisWeek_dict ={}
	week_of_season = ""
	# strlength
# 	posOfweek
# 	thisWeek
	
	for row in table[0].findAll('tr'):
		line=[]
		for cell in row.findAll('td'):
			line.append(cell.text)
		first_element = str(line[0:1]).strip("['']").strip("u'").replace('\\xa0','')
		first_element_length = len(first_element)	
		if len(line)==1:
			week_of_season = str(line).strip("[u'']")
			strlength = len(week_of_season)
			posOfweek = week_of_season.find("Week")
			thisWeek = week_of_season[posOfweek+5:]
			team_dict['week'] = thisWeek
			players_dict['week'] = thisWeek
			position = week_of_season[:posOfweek]
			players_dict['position'] = position
 	
			
		if first_element.isdigit() and first_element_length >= 1:
			matchupStr=str(line[1:2]).strip("[u'").rstrip(" [+]'").replace('\\xa0','')
			vs_pos = matchupStr.find("vs")
			opp_team = matchupStr[:vs_pos-4]
			team_mascot = matchupStr[vs_pos+3:-1]
			team_dict['opp_team'] = opp_team
			players_dict['team'] = opp_team
			team_dict['team_mascot'] = team_mascot
			team_dict['weekly_stat'] = line[2:-1]
		elif len(line)==14 and first_element_length ==0:
			 playerList(line)

	if players_dict in players:
		print("True")
		theList(players)
	else:
		print("adding ",players_dict)
		players.append(players_dict)
		theList(players)
	# print(len(players),players_dict,players)
	print("\n")	
	
	
# 	search_players_dict('Roethlisberger, Ben',players)
			
# 		print(team_dict)
# 		players.append(players_dict)
# 		teams.append(team_dict)
# 	print(teams)
	# theList(players)
# 	searchDict("Steelers",teams)



def theList(alist):
	for dict in alist:
		print("dict:",dict)
		
def searchDict(name,alist):
	for d in alist:
		if d['team_mascot'] == name:
			print(d)
			
def search_players_dict(name,alist):
	for d in alist:
		if d['name'] == name:
			print(d)
			
# 	print([element for element in teams if element['opp_team'] == 'Steelers'])
# 	filtered_list = filter(lambda team_dict: team_dict['opp_team'] == 'Steelers', teams)
# 	print(filtered_list)		




def getPlayers(tr):
    qb_stats = ['Att', 'Cmp', 'Yd', 'TD', 'Int', 'Rate', 'Att', 'Yd', 'Avg', 'TD', 'FL', 'FPTS']
    table_rows = tr
    for row in table_rows:	
        player1(row)
          #   if len(temp2) >0 :
# 				matchupStr = str(player[1:2]).strip("[u'").rstrip(" [+]'").replace('\\xa0','')
# 				matchupStr.strip("[u'")
# 				vs_pos = matchupStr.find("vs")
# 				opp_team = matchupStr[:vs_pos-3]
# 				team_mascot = matchupStr[vs_pos+3:-1]
# 				team_dict['opp_team'] = opp_team
# 				team_dict['team_mascot'] = team_mascot	
# 			teams.append(team_dict)
# 	print(teams)
# # print("\n")


def player1(row):
	print("func player1(row)")
	player=[]
	print(row) 
	for cell in tr.findAll('td'):
		print(cell.text)
		player.append(cell.text)
		temp = str(player[0:1]).strip("['']").strip("u'").replace('\\xa0','')
	print(player)
print("\n") 
# 		
    	
    	
    	

        
		 
		 
		 
		 
		 
		 
# 		pass
# 	else:
# 		line =str(player).strip("[]").strip("u'") 
# 		
# 		if "Week" in line:
# 			print()
# 			line_striped = line.strip("[u' ']")
# 			print(line_striped)
# 			print(line)
# 		if "Rank" in line:
# 			stat_headers = line.strip("[u' ']")
# 			print(stat_headers)
     #    if len(temp2) == 0:
# 			print("\n")
# 		else:
# 			print(temp2)
		
# 	print("player",player)

            
			
			
			
			
			
			
		
            
            
            
            
            
	
#     print(line)
#         
#             if len(temp2) == 0:
# 				player_name = player[1:2]
# 				# print(str(player_name).strip("[u'']"))
# 				players_dict['name'] = str(player_name).strip("[u'']")
# 				players_dict['weekly_stats'] = str(player[2:-1])
# 			else:
# 				line =str(player).strip()
# 				print(line)
# 				
# 	  #   	else:
# # 				line =str(player).strip()
# # 				print(line)
# 
# 			print("\n")

      
# 		if "QB" in team_stripped:
# 			qb = team_stripped.find("QB")
# # 				print(team_stripped[:qb])
# 			players_dict['team'] = team_stripped[:qb]
# 			nx = qb+6
# # 				print(team_stripped[qb+6:-1])
# 			team_stats = {'week':week,'stat':player[2:-1]}
# 			# print(team_stats)
# 			team_dict['team_name'] = team_stripped[qb+6:-1]
# 			team_dict['stats'] = team_stats
# 			print("List Of Teams:",teams)
# 			teams.append(team_dict)
# 			break;
			# print(team_dict)
# 			if teams.append(team_dict):
# 				print(teams)
# 			if team_dict in teams:
# 				print("true")
# 				print(team_dict)
# # 					
# 				else:
# 					print("false")
					# print(team_dict)
# 					teams.append(team_dict)
# 					print(teams)
				# teams.append(team_dict)
# 				print(team_dict)
# 				print(teams)
			# 	if team_dict not in teams:
# 					teams.append(team_dict)
# 					print(team_dict)
# 					print(teams)
# 				print(team_dict)
				# players_dict['team'] = team_stripped[:qb]
# 				players_dict['opp'] = team_stripped[qb+6:-1]
# 		players.append(players_dict)
# 		



for pos in positions:
	temp = base_url+pos
	type = str(stat_type[0:1]).strip("['']")
	for week in range(1,18):
		fullUrl=base_url+pos+"/all/"+str(week)+"/"+type
		my_soup = returnSoup(fullUrl)
		mytext = my_soup.get_text(strip=True)
		doc_table = my_soup.findAll("table")
		table_rows(doc_table)
	# 	html = urlopen(fullUrl)
# 		bsObj = BeautifulSoup(html,'lxml')
		
	# 	doc_table = bsObj.findAll("table")
	
	# 	print(len(doc_table))
# 		print(str(doc_table).strip("[]"))
		# for tr in doc_table:
# 			getPlayers(tr)
			