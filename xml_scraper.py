from bs4 import BeautifulSoup
import pdb;pdb.set_trace()


xml_source = "comicBook3.xml"
infile = open(xml_source,"r")
contents = infile.read()
soup = BeautifulSoup(contents,'xml')
series = soup.find_all('series')
titles = soup.find_all('title')
volumes = soup.find_all('vol')
years = soup.find_all('year')
publishers = soup.find_all('publisher')
quantity = soup.find_all('qty')
prices  = soup.find_all('price')
for i in range(0,len(series)):
	print()
	print(series[i].get_text().strip(),end=' ')
	print(titles[i].get_text().strip(),end = ' ')
	print(volumes[i].get_text().strip(),end = " ")
	print(years[i].get_text().strip(),end = " ")
	print(publishers[i].get_text().strip(),end = ' ')
	print(quantity[i].get_text().strip(),end = ' ')
	print(prices[i].get_text().strip(),end = ' ')
	print()
