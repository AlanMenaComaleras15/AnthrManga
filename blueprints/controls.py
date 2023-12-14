from flask import *
import os
from modules import db, utilities

controls = Blueprint('controls', __name__)

@controls.route('/addreading/<book>/<chapter>/<order>')
def addreading(book, chapter, order):
    activeid = request.cookies.get('uuid')
    db.addreading(book, activeid, chapter, order) # Checks if is added and adds it if necessary.

    return redirect(f'/manga/reader/{chapter}')

@controls.route('/removereading/<chapter>')
def removereading(chapter):
    activeid = request.cookies.get('uuid')
    db.removereading(chapter, activeid) # Checks if is added and adds it if necessary.

    return redirect(f'/manga/reader/{chapter}')

@controls.route('/buy/<bookID>/<chapterID>')
def buy(bookID, chapterID):
    activeid = request.cookies.get('uuid')

    db.addlibrary(bookID, activeid, chapterID)
    return redirect(f'/feed/details/{bookID}')

@controls.route('/bulkbuy/<bookID>')
def bulkbuy(bookID):
    activeid = request.cookies.get('uuid')

    db.addlibraryinbulk(bookID, activeid)
    return redirect(f'/feed/details/{bookID}')

@controls.route('/next/<bookID>/<chapterID>')
def next(bookID, chapterID):
    
    next = utilities.getnextchapter(bookID, str(chapterID))

    if next == None:
        return redirect(f'/feed/details/{bookID}')

    return redirect(f'/manga/reader/{next}')

@controls.route('/previous/<bookID>/<chapterID>')
def previous(bookID, chapterID):
    
    previous = utilities.getpreviouschapter(bookID, str(chapterID))

    if previous == None:
        return redirect(f'/feed/details/{bookID}')

    return redirect(f'/manga/reader/{previous}')


@controls.route('/search')
def search():
    return render_template('search.html')

@controls.route('/results', methods = ['POST','GET'])
def results():
    print("TEST")
    query = request.form['text']

    results = db.search(query)
    resultsLen = len(results)

    return render_template('results.html', resultsLen=resultsLen, results=results)