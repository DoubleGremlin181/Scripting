#A script to check if any two wikipedia pages have any common wiki links
#TODO: Check on multiple levels, i.e. check if any of the linked wikis on the pages have a common wiki link

import requests
import wikipedia
from bs4 import BeautifulSoup


def get_list(page):

    links_page=["/wiki/"+page.split("/")[4]]
    data = requests.get(page).content
    soup = BeautifulSoup(data, "lxml")

    for temp in  soup.find_all("a"):
        if temp.parent.name =="p":
            links_page.append(temp["href"])

    return links_page
def compare(list1,list2):

    common=[]
    for i in list1:
        if i in list2:
            common.append("https://en.wikipedia.org"+i)

    return common

def main():

    page1 = raw_input("Enter the url of the first page\n>")
    page2 = raw_input("Enter the url of the second page\n>")
    links_page1=get_list(page1)
    links_page2=get_list(page2)

    common = compare(links_page1,links_page2)

    print "\nThe pages are directly linked through the following wikis:\n"
    print '\n'.join(['%i: %s' % (n+1, common[n]) for n in xrange(len(common))])


if __name__ == '__main__':
    main()
