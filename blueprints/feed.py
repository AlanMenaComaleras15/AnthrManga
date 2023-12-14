from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)
from templates import templatesconstants
from modules import db, utilities

feed = Blueprint('feed', __name__)

@feed.route('/')
def returnfeed():
    activeid = request.cookies.get('uuid')
    if activeid != None:
        user = db.isloggedin(activeid)
        if user:
            structure = ["CRT.html", "CRG.html", "LT.html", "LG.html", "N.html", "N.html", "DT.html", "DG.html", "N.html", "N.html"]

            reading = user[0]["reading"]["reading"]
            library = user[0]["books"]["books"]
            discover = utilities.getrandombooks()
            discoverCount = len(discover)
            readingCount = len(reading)
            libraryCount = len(library)

            if readingCount == 0:
                structure[0] = "LT.html"
                structure[1] = "LG.html"

            if libraryCount == 0:
                structure = ["DT.html", "DG.html", "DT.html", "DG.html", "N.html", "N.html", "N.html", "N.html", "N.html", "N.html"]

            username = utilities.getusername(user)

            return render_template('feed.html', structure=structure, username=username, reading=reading, readingCount=readingCount, library=library, libraryCount=libraryCount, discover=discover, discoverCount=discoverCount)
        else:
            resp = make_response(redirect('/sessions/loginform'))
            resp.set_cookie('uuid', expires=0)
            return resp
    else:
        discover = utilities.getrandombooks()
        discoverCount = len(discover)

        structure = ["N.html", "N.html", "N.html", "N.html", "N.html", "N.html", "DT.html", "DG.html", "N.html", "N.html"]
        return render_template('feed.html', structure=structure, username='Login', discover=discover, discoverCount=discoverCount)

@feed.route('/details/<bookID>')
def returndetails(bookID):
    activeid = request.cookies.get('uuid')
    if activeid != None:
        user = db.isloggedin(activeid)[0]
        if user:
            book = db.getbookbyid(bookID)

            chaptersOwned = None #This is the default value of chaptersOwned

            for bookOwned in user['books']['books']:
                if bookID == bookOwned['bookID']:
                    chaptersOwned = bookOwned
                    print(chaptersOwned['chapters'])

            return render_template('details.html', book=book, totalchapters=len(book['chapters']), chapters=db.getchaptersbyidarray(book['chapters']), chaptersOwned=chaptersOwned)

    return redirect("/sessions/loginform")

@feed.route('/library')
def library():
    activeid = request.cookies.get('uuid')

    return(db.isloggedin(activeid)[0]['books'])
