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

def getMangaURL(n):
    baseURL = "http://www.mangaeden.com/en/en-manga/"
    formatedName = n.lower().strip().replace(' ','-')
    extractedData = extractData(baseURL + formatedName + "/")
    if extractedData.title.string == "\n404 NOT FOUND - Manga Eden\n":
    	print "404 NOT FOUND"
    	exit()
    return baseURL + formatedName + "/"

def extractData(getDataURL):
    page = requests.get(getDataURL).content
    soup = BeautifulSoup(page, "lxml")
    return soup

def getMangaDescription(mangaURL):
    return extractData(mangaURL).find("h2",{"id":"mangaDescription"}).string

def makeFolder(path):
    if not os.path.exists(path):
		os.mkdir( path, 0755 )
    pass

def downloadImage(pageNo,chapterPath,chapterURL):
    if glob.glob(chapterPath + "/" + str(pageNo) + "*"):
        return
    imageURL = "https:" + extractData(chapterURL + "/" + str(pageNo)).find("a",{"id":"nextA"}).find("img")["src"]
    imgData = requests.get(imageURL)
    img = Image.open(BytesIO(imgData.content))
    img.save(chapterPath + "/" + str(pageNo) + imageURL[imageURL.rfind("."):])
    pass


def downloadChapter(chapterURL,path):
    lastPage = int(extractData(chapterURL).find_all("option")[-1].get_text())
    for i in range(1, lastPage + 1):
        downloadImage(i,path,chapterURL)
        print ("Progress: Page "+str(i)+" of "+str(lastPage))
    print "Download complete"
    pass

def open(path):
    ch = raw_input("\nDo you want to open the chapter? yes or no\n> ")
    if ch == "y" or ch == "yes":
        print "Opening chapter"
        subprocess.call(["eog", glob.glob(path + "/1.*")[0]])
    elif ch == "n" or ch == "no":
        exit()
    else:
        print "Invalid input"
    pass

def main():
    n = raw_input("Enter the name of the manga\n> ")
    mangaURL = getMangaURL(n)
    print "\nManga Description:\n" + getMangaDescription(mangaURL)
    ch = raw_input("Do you want to download a chapter?\n> ")
    if ch == "y" or ch == "yes":
        makeFolder(n)
        chapterNo = raw_input("Enter the chapter number\n> ")
        makeFolder(n + "/" + chapterNo)
        downloadChapter(mangaURL+chapterNo,n + "/" + chapterNo)
        open(n + "/" + chapterNo)
    elif ch == "n" or ch == "no":
    	exit()
    else:
    	print "Invalid input"
    pass

if __name__ == '__main__':
    main()
