""" DISCLAIMER:Use at your own risk:
This script is solely made for academic purposes.
Downloading content via this script may be illegal in your country. I am not to blame for any such issues.
Please support the official releases """

import requests
import glob
import os
import subprocess
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def mangaURL(n):
    base_url = "http://www.mangaeden.com/en/en-manga/"
    name = n.lower().strip().replace(' ','-')
    return base_url + name + "/"


def extractData(manga_url):
    page = requests.get(manga_url).content
    soup = BeautifulSoup(page, "lxml")
    return soup

def mangaDescription(desc_page,n):
    mangaDescription = desc_page.find("h2",{"id":"mangaDescription"}).string
    print "\nManga Description:\n" + mangaDescription
    pass

def makeFolder(path):
    if not os.path.exists(path):
		os.mkdir( path, 0755 )
    pass

def imageURL(page_no,chapter_url):
    page_url = chapter_url + str(page_no)
    page_data = extractData(page_url)
    img_block = page_data.find("a",{"id":"nextA"})
    img_tag = img_block.find("img")["src"]
    return "https:" + img_tag

def downloadImage(page_no,chapter_path,chapter_url,last_page):
    if glob.glob(chapter_path + "/" + str(page_no) + "*") and page_no != 1:
        print ("Progress: Page "+str(page_no)+" of "+str(last_page))
        return
    img_url = imageURL(page_no,chapter_url)
    ext = img_url[img_url.rfind("."):]
    img_name = chapter_path + "/" + str(page_no) + ext
    img_data = requests.get(img_url)
    img = Image.open(BytesIO(img_data.content))
    img.save(img_name)
    print ("Progress: Page "+str(page_no)+" of "+str(last_page))
    pass

def downloadChapter(n,manga_url):
    chapter_path=""
    chapter_url=""
    last_page=""

    makeFolder(n)
    chapter = raw_input("Enter the chapter number\n> ")
    chapter_path = n + "/" + chapter
    makeFolder(chapter_path)
    chapter_url = manga_url + chapter +"/"
    page1_data = extractData(chapter_url)
    last_page = int(page1_data.find_all("option")[-1].get_text())
    for i in range(1, last_page + 1):
        downloadImage(i,chapter_path,chapter_url,last_page)
    print "Download complete"
    open(chapter_path)
    pass

def open(chapter_path):
    ch = raw_input("\nDo you want to open the chapter? yes or no\n> ")
    if ch == "y" or ch == "yes":
        print "Opening chapter"
        subprocess.call(["eog", glob.glob(chapter_path + "/1.*")[0]])
    elif ch == "n" or ch == "no":
        exit()
    else:
        print "Invalid input"
    pass

def main():
    n =""
    n = raw_input("Enter the name of the manga\n> ")
    manga_url = mangaURL(n)
    desc = extractData(manga_url)
    if desc.title.string == "\n404 NOT FOUND - Manga Eden\n":
    	print "404 NOT FOUND"
    	exit()
    mangaDescription(desc,n)
    ch = raw_input("Do you want to download a chapter?\n> ")
    if ch == "y" or ch == "yes":
        downloadChapter(n,manga_url)
    elif ch == "n" or ch == "no":
    	exit()
    else:
    	print "Invalid input"
    pass

if __name__ == '__main__':
    main()
