""" DISCLAIMER:Use at your own risk:
This script is solely made for academic purposes.
Downloading content via this script may be illegal in your country. I am not to blame for any such issues.
Please support the official releases """

import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

base_url = "http://www.mangaeden.com/en/en-manga/"

n = raw_input("Enter the name of the manga\n> ")
name = n.lower().strip().replace(' ','-')
url = base_url + name + "/"
page = requests.get(url).content
soup1 = BeautifulSoup(page, "lxml")
if soup1.title.string == "\n404 NOT FOUND - Manga Eden\n":
	print "404 NOT FOUND"
	exit()
mangaDescription = soup1.find("h2",{"id":"mangaDescription"}).string
print "\nManga Description:\n" + mangaDescription
ch = raw_input("Do you want to download a chapter?\n> ")
if ch == "y" or ch == "yes":
	if not os.path.exists(n):
		os.mkdir( n, 0755 )
	chapter = raw_input("Enter the chapter number\n> ")
	chapter_path = n + "/" + chapter
	if not os.path.exists(chapter_path):
		os.mkdir(chapter_path , 0755 )
	chapter_url = url + chapter +"/"
	page1_data  = requests.get(chapter_url).content
	soup2 = BeautifulSoup(page1_data, "lxml")
	last_page = int(soup2.find_all("option")[-1].get_text()) 
	for i in range(1,last_page+1):
		page_url = chapter_url + str(i)
		page_data = requests.get(page_url).content
		soup3 = BeautifulSoup(page_data,"lxml")
		img_block = soup3.find("a",{"id":"nextA"})
		img_tag = img_block.find("img")["src"]
		img_url = "https:" + img_tag
		ext = img_url[img_url.rfind("."):]
		img_name = chapter_path + "/" + str(i) + ext
		if os.path.exists(img_name):
			print ("Progress: Page "+str(i)+" of "+str(last_page))
			continue
		img_data = requests.get(img_url)
		img = Image.open(BytesIO(img_data.content))
		img.save(img_name)
		print ("Progress: Page "+str(i)+" of "+str(last_page))
	print "Download complete"
	ch = raw_input("\nDo you want to open the chapter? yes or no\n> ")
	if ch == "y" or ch == "yes":
		print "Opening chapter"
		image = Image.open(chapter_path + "/1" + ext)
		image.show()
	elif ch == "n" or ch == "no":
		exit()
	else:
		print "Invalid input"
		
elif ch == "n" or ch == "no":
	exit()
	
else:
	print "Invalid input"
