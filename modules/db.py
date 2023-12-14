import os
import uuid
import supabase
from supabase import *
from datetime import datetime
import json
from pathlib import Path
from modules import utilities
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print(url)
print(key)

supabase: Client = create_client(url, key)

USERS_TABLE = 'users'
BOOKS_TABLE = 'books'
CHAPTERS_TABLE = 'chapters'

COVERS_BUCKET = 'covers'
CHAPTERS_BUCKET = 'epub'

def newuser(pswd, email):
    """Function that creates a new user in the DB and returns its activeID.

    Args:
        pswd (str): Password that the user desires
        email (str): User's email
    """
    activeid = str(uuid.uuid4())

    json_request = {
    "id": str(uuid.uuid4()),
    "activeid": activeid,
    "password": hash(pswd),
    "email": email,
    "timestamp": str(datetime.now()),
    "subscribed": False,
    "publisher": False,
    "books": {
        "books": []
    },
    "reading": {
        "reading": []
        }
    }

    data, count = supabase.table(USERS_TABLE).insert(json_request).execute()

    return(activeid)

def getlogininfo(email, password):
    """Takes the password of the user and checks that it matches the DB password.

    Args:
        email (str): Email of the user
        password (str): Password to check

    Returns:
        _type_: Can return Flase if the password or user does not match or can return the user.
    """

    password = hash(password)
    print(password)
    user = supabase.table(USERS_TABLE).select("*").eq('email', email).execute()
    user = user.json()
    user = json.loads(user)
    user = user["data"][0]
    if str(user['password']) == str(password):
        return user
    else:
        return False

def isloggedin(activeid):
    """Returns user data if it has a valid activeID

    Args:
        activeid (uuid): uuid to check for user.
    """
    try:
        user = supabase.table(USERS_TABLE).select("*").eq('activeid', activeid).execute()
        user = user.json()
        user = json.loads(user)
        return(user['data'])
    except:
        return None


def logout(activeid):
    """Invalidates and creates a new activeID for the user.

    Args:
        activeid (uuid): The activeID to invalidate
    """

    new_values = {"activeid": str(uuid.uuid4())}
    supabase.table(USERS_TABLE).update(new_values).eq("activeid", activeid).execute()

def addbook(title, author, pubID, price, description, language, cover, public):
    """Adds a new book to the DB

    Args:
        title (str): Title of the book
        author (str): Public name of the author
        pubID (str): ID of the publisher
        price (float): Price of the whole book
        description (str): Desctiption of the book
        language (str): Language code of the book
        cover (uuid): UUID of the cover image
        public (bool): Sets the visibility of the book
    """

    json_request = {
    "name": title,
    "author": author,
    "publisher": pubID,
    "price": price,
    "description": description,
    "language": language,
    "cover": cover, 
    "public": public,
    "chapters": []
    }

    supabase.table(BOOKS_TABLE).insert(json_request).execute()

def addcover(cover, coverID):
    """Adds a cover to the storage bucket

    Args:
        cover (str): path of the cover
        coverID (str): coverID
    """

    with open(str(cover), 'rb+') as f:
        res = supabase.storage.from_(COVERS_BUCKET).upload(f'{coverID}.jpg', f.read())

def addprice(cover, price):
    updateValues = {
        "price": price
    }
    supabase.table(BOOKS_TABLE).update(updateValues).eq("price", cover).execute()

def getbookbyid(bookID):
    book = supabase.table(BOOKS_TABLE).select("*").eq('id', bookID).execute()
    book = json.loads(book.json())

    return(book['data'][0])

def addchapter(title, description, order, epubID, bookID):
    book = supabase.table(BOOKS_TABLE).select("*").eq('id', bookID).execute()
    book = json.loads(book.json())['data'][0]

    json_request = {
    "name": title,
    "description": description,
    "order": order,
    "price": 8,
    "book": book['id']
    }

    chapter = supabase.table(CHAPTERS_TABLE).insert(json_request).execute()

    chapter = json.loads(chapter.json())['data'][0]

    # with open(str(f'epub/{epubID}.epub'), 'rb+') as f:
    #     res = supabase.storage.from_(CHAPTERS_BUCKET).upload(f'{chapter["id"]}.epub', f.read())

    appender = [str(chapter["id"])]
    appendedchapters = book['chapters'] + appender
    updateValues = {
        "chapters": appendedchapters
    }

    supabase.table(BOOKS_TABLE).update(updateValues).eq("id", bookID).execute()

    return(chapter['id'])

def getchaptersbyidarray(array):
    chapters = []

    for chapter in array:
        chapter = supabase.table(CHAPTERS_TABLE).select("*").eq('id', chapter).execute()
        chapter = json.loads(chapter.json())['data'][0]

        chapters.append(chapter)
    
    return(chapters)

def haspermissiontoedit(activeID, bookOwner):
    user = supabase.table(USERS_TABLE).select("*").eq('activeid', activeID).execute()
    user = json.loads(user.json())['data'][0]

    if user['email'] == bookOwner:
        return True
    else:
        return False

def canupload(activeID):
    user = supabase.table(USERS_TABLE).select("*").eq('activeid', activeID).execute()
    user = json.loads(user.json())['data'][0]

    if user['publisher']:
        return(True)
    else:
        return(False)

def getchapterbyid(chapterID):
    chapter = supabase.table(CHAPTERS_TABLE).select("*").eq('id', chapterID).execute()
    try:
        return(json.loads(chapter.json())['data'][0])
    except:
        return(False)

def getbook(book):
    print("GETTING BOOK")
    if Path(f'bibi-bookshelf/{book}').is_file():
        pass
    else:
        with open(f'bibi-bookshelf/{book}', 'wb+') as f:
            res = supabase.storage.from_(CHAPTERS_BUCKET).download(book)
            f.write(res)

def geturl(book):
    res = supabase.storage.from_(CHAPTERS_BUCKET).create_signed_url(f'/{book}', 1200)

    return(res['signedURL'])

def getpublicurl(book):
    #res = supabase.storage.from_(CHAPTERS_BUCKET).get_public_url(f'/{book}')
    return("Somethong")

def addreading(book, user, chapter, order):
    user = supabase.table(USERS_TABLE).select("*").eq('activeid', user).execute()
    user = json.loads(user.json())['data'][0]
    bookdata = getbookbyid(book)

    for books in user['reading']['reading']:
        if books['chapter'] == chapter:
            return False

    for books in user['reading']['reading']:
        if books['bookID'] == book:
            books['chapter'] = chapter
            books['order'] = order
            supabase.table(USERS_TABLE).update(user).eq("activeid", user['activeid']).execute()
            return(True)


    user['reading']['reading'].append({
        "bookID": book,
        "chapter": chapter,
        "order": order,
        "author": bookdata['author'],
        "cover": bookdata['cover'],
        "name": bookdata['name']
        })

    print(user['reading']['reading'])

    updateValues = user['reading']
    print(updateValues)

    supabase.table(USERS_TABLE).update(user).eq("activeid", user['activeid']).execute()

def removereading(chapter, user):
    user = supabase.table(USERS_TABLE).select("*").eq('activeid', user).execute()
    user = json.loads(user.json())['data'][0]

    for books in user['reading']['reading']:
        if books['chapter'] == chapter:
            user['reading']['reading'].remove(books)

            supabase.table(USERS_TABLE).update(user).eq("activeid", user['activeid']).execute()
            return(True)

def addlibrary(bookID, user, chapter):
    """Adds a chapter to the library of a given user

    Args:
        book (int): bookID
        user (uuid): activeID
        chapter (int): chapterID
    """
    user = supabase.table(USERS_TABLE).select("*").eq('activeid', user).execute()
    user = json.loads(user.json())['data'][0]

    book = getbookbyid(bookID)

    # First we check if we have the book
    for bookIterated in user['books']['books']:
        if bookIterated['bookID'] == bookID:
            # We HAVE the book
            # So we APPEND a chapter
            bookIterated['chapters'].append(chapter)

            supabase.table(USERS_TABLE).update(user).eq("activeid", user['activeid']).execute()
            return(True)

    # We DON'T HAVE the book
    # So we CREATE the book and APPEND the chapter

    user['books']['books'].append({
        "bookID": bookID,
        "chapters": [chapter],
        "name": book['name'],
        "author": book['author'],
        "cover": book['cover']
        
    })

    supabase.table(USERS_TABLE).update(user).eq("activeid", user['activeid']).execute()

def addlibraryinbulk(bookID, user):
    """Adds a book to the library of a given user

    Args:
        book (int): bookID
        user (uuid): activeID
    """
    user = supabase.table(USERS_TABLE).select("*").eq('activeid', user).execute()
    user = json.loads(user.json())['data'][0]

    book = getbookbyid(bookID)

    # First we check if we have the book
    for bookIterated in user['books']['books']:
        if bookIterated['bookID'] == bookID:
            # We HAVE the book
            # So we add all the chapters
            bookIterated['chapters'] = book['chapters']
            
            supabase.table(USERS_TABLE).update(user).eq("activeid", user['activeid']).execute()
            return(True)

    # We DON'T HAVE the book
    # So we CREATE the book and APPEND the chapter

    user['books']['books'].append({
        "bookID": bookID,
        "chapters": book['chapters'],
        "name": book['name'],
        "author": book['author'],
        "cover": book['cover']
    })

    supabase.table(USERS_TABLE).update(user).eq("activeid", user['activeid']).execute()


def getallbookIDs():
    """Gets all bookIDs
    """
    
    # Select all values from the "column_name" column of the "table_name" table
    result = supabase.table(BOOKS_TABLE).select("*").execute()

    result = json.loads(result.json())['data']

    # Print the array of values
    return(result)

def search(term):
    results = json.loads(supabase.table(BOOKS_TABLE).select("*").text_search('name', str(term)).execute().json())['data']

    return(results)