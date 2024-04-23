from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
from collections import deque
import re

def connectDB():
    DB_NAME = "crawler"
    DB_HOST = "localhost"
    DB_PORT = 27017

    client = MongoClient(DB_HOST, DB_PORT)
    db = client[DB_NAME]
    return db

def crawlerThread(frontier):
    #while frontier is not empty
    while frontier:
        url = frontier.popleft()
        #fix url
        if(re.match("^https://www.cpp.edu", url) == None):
            url = "https://www.cpp.edu" + url
        #store html
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        #store in db
        pages.insert_one({"url": url, "html": str(bs)})
        vis.add(url)
        #check if target page is found
        if bs.find("h1", string="Permanent Faculty"):
            print("Target page found")
            frontier.clear()
        else:
            #add links to frontier
            for links in bs.find_all("a", href=True):
                link = links["href"]
                if(re.match("^https://www.cpp.edu", link) == None):
                    link = "https://www.cpp.edu" + link
                #check if link is not visited
                if link not in vis:
                    frontier.append(link)

db = connectDB()
pages = db.pages

frontier = deque()
frontier.append("https://www.cpp.edu/sci/computer-science")
vis = set()
crawlerThread(frontier)
