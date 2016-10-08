import requests
from bs4 import BeautifulSoup

n = raw_input("Enter a movie/TV series name\n> ")
name = n.strip().replace(' ','+')
url = "http://www.omdbapi.com/?t="+ name +"&y=&plot=short&r=xml"
page = requests.get(url).content
soup = BeautifulSoup(page, "lxml")
if soup.find("error") != None:
	print "Movie/TV Series not found!"
	exit()
title = soup.find("movie")["title"]
actors = soup.find("movie")["actors"]
genre = soup.find("movie")["genre"]
plot = soup.find("movie")["plot"]
year = soup.find("movie")["year"]
runtime = soup.find("movie")["runtime"]
imdbrating = soup.find("movie")["imdbrating"]
metascore = soup.find("movie")["metascore"]

print title+" ("+year+") |Genre: "+genre+" | "+runtime+"\nIMDB Rating: "+imdbrating+"\tMetacritic score: "+metascore+"%\n\nActors: "+actors+"\n\nPlot: "+plot
