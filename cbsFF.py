import requests
import csv
import string
from lxml import html,etree
from bs4 import BeautifulSoup
import pdb;pdb.set_trace()

players=[]
baseUrl='https://www.cbssports.com/fantasy/football/stats/'
positions=['QB','RB','WR','TE','DST']
years=['2019','2018','2017']
stats='/season/stats/ppr/'


def writeCSVFile(file,headers,players):
    writeFile(file,headers)
    writeFile1(file,players)

def returnTree(a_url):
    response = requests.get(a_url)
    page = response.content
    return html.fromstring(page)

def returnSoup(a_url):
    response = requests.get(a_url)
    page = response.content
    return BeautifulSoup(page,'lxml')

def writeFile(file,line):
      writer = csv.writer(open(file,"a+"))
      writer.writerow(line)

def writeFile1(file,players):
      writer = csv.writer(open(file,"a+"))
      writer.writerows(players)

def create_fullPath(baseUrl,pos,year,stats):
    return baseUrl+pos+"/"+years[year]+stats

def create_fileName(baseUrl,pos,year,stats):
    fileName = create_fullPath(baseUrl,pos,year,stats)
    return fileName.split("/")

def tableHeaders(table):
    for th in table[0].findAll('th'):
        header = []
        for cell in th.findAll('td'):
            line.append(cell.text.strip())

def tableRow(table,fname):
    for tr in table[0].findAll('tr'):
        line = []
        for cell in tr.findAll('td'):
            if len(cell.text.replace("\n",'').split())> 1:
                line = cell.text.replace("\n",'').split()
            else:
                line.append(cell.text.strip())
        players.append(line)
        writeFile(fname,line)
    printPlayers(players)

def printPlayers(players):
	for player in players:
		print(player)


def main():
    year = 0
    while year < 3:
    	for pos in positions:
            print(baseUrl+pos+"/"+years[year]+stats)
            fullPath = baseUrl+pos+"/"+years[year]+stats
            fileName = pos+"_"+years[year]+".csv"
            print(fileName)
            myTree = returnTree(fullPath)
            newSoup = returnSoup(fullPath)
            r_table = newSoup.findAll('table')
            tableRow(r_table,fileName)
    	year += 1

main()







  	  # 	for cell in tr.findAll('td'):
#   	  		print(cell.text)
#   	  		line.append(cell.text)
#   	  		value = line[0:1]
#   	  	print(line,len(line))
  	  	# if len(line) == 1:
#   	  		get_position_week(line)
#   	  	if len(line) == 14 and "Rank" in line[0:1]:
#   	  		print("Headers",line[1:])
#   	  		stat_lables = line[2:-1]
#   	  	if len(line) == 14 and str(value).strip("['']").isdigit():
#   	  		print("Matchup", line)
#   	  	if len(line) == 14 and str(value).strip("['']").isdigit() == False and "Rank" not in line[0:1]:
#   	  	    create_player_dict(line)
#   	  	    players.append(line)
#   	  	print()
