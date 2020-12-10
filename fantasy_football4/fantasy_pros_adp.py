
from urllib import urlopen
from bs4 import BeautifulSoup
import pymysql.cursors

fantasy_pros_url = 'https://www.fantasypros.com/nfl/adp/ppr-overall.php'
html = urlopen(fantasy_pros_url)

bsObj = BeautifulSoup(html,"lxml")
mobile_table = bsObj.find("div", {"class": "mobile-table"})
player_table = mobile_table.table
rows=[]
headers=[]
player=[]
players=[]

# print(player_table)
for th in player_table.findAll("th"):
	headers.append(str(th.get_text()))
print(headers)
for tr in player_table.findAll("tr"):
	player=[]
	for td in tr.findAll("td"):
		
		player.append(map(str,td))
	# print(player)
	players.append(player)
print(players)
# print(len(doc_table))
# print(len(doc_table[0].findAll("tr")))
# for th in doc_table[0].findAll("th"):
# 	print(th.get_text())
# 	headers.append(str(th.get_text()))
# for tr in doc_table[0].findAll("tr"):
# 	row=[]
# 	player = tr.get_text()
# 	player = str(player)
# 	for td in tr.findAll('td'):
# 		print(str(td.get_text()))
# 		row.append(str(td.get_text()))
# 	rows.append(row)