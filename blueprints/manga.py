from flask import *
from modules import db, utilities
import uuid, os, random
from urllib.parse import urlparse
from werkzeug.utils import secure_filename

MAINURL = "/feed"
manga = Blueprint('manga', __name__)

@manga.route('/')
def returntomain():
	return redirect(MAINURL)

@manga.route('/addmangastep1form', methods = ['POST','GET'])
def addmangastep1form():
	return render_template('addmangastep1.html')

@manga.route('/addmangastep1', methods = ['POST','GET'])
def addmangastep1():
	if request.method == 'POST':
		activeID = request.cookies.get('uuid')
		if activeID == None:
			return(redirect('/'))

		if db.canupload(activeID) == False:
			return(redirect('/'))


		coverID = str(uuid.uuid4())
		coverPath = os.path.join('modules/covers', f'{coverID}.jpg')

		mangaName = request.form['title-input']
		mangaDescription = request.form['description']
		mangaAuthor = request.form['author-input']
		#mangaCategories = request.form['mangaCategories']
		isFinished = request.form['status']
		#isPublic = request.form['isPublic']
		#mangaCountries = request.form['mangaCountries']
		#mangaPrice = request.form['mangaPrice']
		mangaLanguage = request.form['language']
		f = request.files['cover']
		f.save(os.path.join('modules/covers/', secure_filename(coverID + '.jpg')))

		user = db.isloggedin(activeID)[0]

		db.addcover(coverPath, coverID)
		price = random.randint(0,99999)
		db.addbook(mangaName, mangaAuthor, user['email'], str(price), mangaDescription, mangaLanguage, f'{coverID}.jpg', True)

		return addmangastep2form(coverID, coverPath, str(price))
	return(redirect('/'))

@manga.route('/addmangastep2form')
def addmangastep2form(coverID, cover, price):
	resp = make_response(render_template('addmangastep2.html', image=coverID))
	resp.set_cookie('coverID', coverID, samesite="Strict")
	resp.set_cookie('price', price, samesite="Strict")
	return resp

@manga.route('/addmangastep2', methods = ['POST','GET'])
def addmangastep2():
	if request.method == 'POST':
		mangaPrice = request.form['price-input']
		coverID = request.cookies.get('coverID')
		price = request.cookies.get('price')
		os.remove(f'modules/covers/{coverID}.jpg')
		db.addprice(price, float(mangaPrice))
		return(returntomain())

@manga.route('/read')
def read():
	book = request.args.get('book')
	return render_template('bibi.html', book=book)

@manga.route('/reader/<id>')
def reader(id):
    chapter = db.getchapterbyid(id)
    if chapter:
        book = db.getbookbyid(chapter['book'])
        chapterid = chapter['id']
        return render_template('reader.html', book=book, chapter=chapter, url=f'{chapterid}.epub')
    else:
        return "Not found", 404

@manga.route('/editor/<bookID>')
def editor(bookID):
    activeid = request.cookies.get('uuid')
    if activeid != None:
        book = db.getbookbyid(bookID)
        print(book)
        if db.haspermissiontoedit(activeid, book['publisher']):
            
            print(book['chapters'])
            return render_template('editor.html', book=book, chapters=db.getchaptersbyidarray(book['chapters']))

@manga.route('/addchapter/<bookID>')
def addchapter(bookID):
	activeid = request.cookies.get('uuid')
	if activeid != None:
		book = db.getbookbyid(bookID)
		if db.haspermissiontoedit(activeid, book['publisher']):
			return render_template('addchapter.html', book=book)
	return(redirect('/'))

@manga.route('/chapteradd/<bookID>', methods = ['POST','GET'])
def chapteradd(bookID):
	if request.method == 'POST':
		activeid = request.cookies.get('uuid')
		
		if activeid != None:
			book = db.getbookbyid(bookID)
			if db.haspermissiontoedit(activeid, book['publisher']):
				epubID = str(uuid.uuid4())
				
				chapterTitle = request.form['title-input']
				chapterDescription = request.form['description']
				chapterOrder = request.form['order']

				f = request.files['epub']

				chapterID = db.addchapter(chapterTitle, chapterDescription, chapterOrder, epubID, bookID)

				f.save(os.path.join('bibi-bookshelf/', secure_filename(str(chapterID) + '.epub')))

	return(returntomain())
