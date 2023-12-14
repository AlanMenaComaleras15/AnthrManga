import json, ast
import random
from modules import db

def getusername(data): #Gets and returns the username from the data
    data = data[0]
    email = data["email"]

    chuncks = email.split("@")
    username = chuncks[0]

    return(username)
 
def getchapters(chapters):
    chapters = ast.literal_eval(chapters)

    return(chapters)

def getnextchapter(book, chapter):
    chapters = db.getbookbyid(book)['chapters']

    i = -1
    for iteratedChapter in chapters:
        i += 1
        if iteratedChapter == chapter:
            try:
                return(chapters[i + 1])
            except:
                return(None)

def getpreviouschapter(book, chapter):
    chapters = db.getbookbyid(book)['chapters']

    i = -1
    for iteratedChapter in chapters:
        i += 1
        if iteratedChapter == chapter:
            if i-1 >= 0:
                return(chapters[i - 1])
            else:
                return(None)

def getrandombooks():
    books = db.getallbookIDs()
    random.shuffle(books)

    return(books)

