import requests
import csv
import string
from lxml import html,etree
from bs4 import BeautifulSoup
import time
import pdb;pdb.set_trace()


position_week = {}
stat_lables = []

def returnSoup(a_url):
    response = requests.get(a_url)
    page = response.content
    return BeautifulSoup(page,'lxml')
    
    
def str2list(string):
	return list(string.split(" "))
	
def list2str(theList):
	return str(theList).strip('[]')
	
def check_for_int(line):
	if str(line[:1]).strip("['']").isdigit():
		return True
	else:
		return False
	
	
def create_team_dict(line):
# 	['32', 'Buccaneers QB vs Saints \xa0[+]', '28', '21', '417', '4', '0', '156.2', '12', '36', '3.00', '1', '0', '49']
	team_dict= {}
	position_matchup = str(line[1:2]).strip('[]')
	line_as_list = str2list(position_matchup)[:4]
	offense = str(line_as_list[0:1]).strip('[]')
	position = str(line_as_list[1:2]).strip('[]')
	defense = str(line_as_list[3:4]).strip('[]')
	stats = str(line[2:-1]).strip('[]')
	p = str(line_as_list[1:2]).strip('[]') 
	print()
	print("Team: ",offense)
	print("Defense: ",defense)
	print("stats :",stats)
	print("position :", p)
	team_dict["Team"] = offense
	team_dict["Defense"] = defense
	team_dict["stats"] = stats
	team_dict["position"] = p
	return team_dict

def fullname(line):
		full_name = line[1:2]	
		player_name =str(line[1:2]).strip('[]')
		firstName = list2str(str2list(player_name)[1:2])
		lastName = list2str(str2list(player_name)[:1])
		return (firstName,lastName)
		
def create_player_dict(line):
	print("player",line,stat_lables)
	player_dict = {}
	player_dict['stats'] = line[2:]
	first_name = fullname(line)[0]
	last_name = fullname(line)[1]
	player_dict["first_name"] = first_name
	player_dict["last_name"] = last_name
	print(player_dict,len(player_dict))
	# print(create_team_dict(line))
	print(dict(zip(stat_lables,map(float,line[2:-1]))))
	return player_dict
	
	
def team_QB_VS_def(value):
	if value[0].isdigit() and len(value[0]) == 1:
          	qb_vs_defense = str(line[1:2]).strip('[]')
          	someStr = str2list(qb_vs_defense)
#           	print(someStr)
          	offense = str(someStr[0:1]).strip('[]')
          	position = str(someStr[1:2]).strip('[]')
          	defense = str(someStr[3:4]).strip('[]')
          	print()
#           	print("Team: ",offense)
          	print("Defense: ",position)
          	teams[offense] = []
          	
def get_position_week(line):
	print(line)
	line = str(line).strip("['']")
	which_week_position = line.find("Week")
	position = line[0:line.find("Week")-1]
	current_week = line[line.find("Week"):]
	position_week["week"] = current_week
	position_week["position"] = position
	return position_week
	

def tableRow(table):
  	  for tr in table[0].findAll('tr'):
  	  	line=[]
  	  	for cell in tr.findAll('td'):
  	  		line.append(cell.text)
  	  		value = line[0:1]
  	  	print(line,len(line))
  	  	if len(line) == 1:
  	  		get_position_week(line)
  	  	if len(line) == 14 and "Rank" in line[0:1]:
  	  		print("Headers",line[1:])
  	  		stat_lables = line[2:-1]
  	  	if len(line) == 14 and str(value).strip("['']").isdigit():
  	  		print("Matchup", line)
  	  	if len(line) == 14 and str(value).strip("['']").isdigit() == False and "Rank" not in line[0:1]:
  	  	    create_player_dict(line)
  	  	    players.append(line)
  	  	print()
  	  			
  	  			
           
          	
          
   
def csv_writer(lines):
	test_file ='cbs_test.csv'
	with open(test_file,'w') as csvfile:
		print('Writing')
		file_writer = csv.writer(csvfile)
		file_writer.writerows(lines)
			
			
			

           
		  
           
     
#=importhtml("https://www.cbssports.com/fantasy/football/stats/posvsdef/QB/all/9/advanced","table")
cbssports_url_base = 'https://www.cbssports.com/fantasy/football/stats/posvsdef/'
testUrl ="https://www.cbssports.com/fantasy/football/stats/posvsdef/QB/all/1/standard"

# positions=['QB','RB','WR','TE']
teams = []
players = []
stat_lables = []

positions=['QB']
for pos in positions:
	player_path = cbssports_url_base+pos+"/all/"
	for week in range(1,2):
		full_url = player_path+str(week)+"/standard"
# 		print(full_url)
		soup = returnSoup(testUrl)
		table = soup.findAll('table') 
		print(pos+ " - Week:"+str(week))
		tableRow(table)
	csv_writer(players)
	for player in players:
		try:
			print(player[1:],len(player))
		except TypeError:
			print("opps")
		
	