from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

def connectDB():
    DB_NAME = "crawler"
    DB_HOST = "localhost"
    DB_PORT = 27017

    client = MongoClient(DB_HOST, DB_PORT)
    db = client[DB_NAME]
    return db

def parseHTML(db):
    pages = db.pages
    professors = db.professors
    #get page
    page = pages.find_one({"url": "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"})
    bs = BeautifulSoup(page['html'], 'html.parser')
    #parse page
    for prof in bs.find_all("div", {"class": "clearfix"}):
        if prof.img:
            #format data
            profData = {
                "name": prof.h2.text,
                "title": prof.p.find("strong", string=re.compile("Title")).next_sibling.replace(":", "").strip(),
                "office": prof.p.find("strong", string=re.compile("Office")).next_sibling.replace(":", "").strip(),
                "phone": prof.p.find("strong", string=re.compile("Phone")).next_sibling.replace(":", "").strip(),
                "email": prof.p.find("a", string=re.compile("@cpp.edu")).text.strip(),
                "website": prof.p.find("a", string=re.compile("cpp.edu/")).text.strip()
            }
            professors.insert_one(profData)

db = connectDB()
parseHTML(db)