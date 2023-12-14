from flask import *
import os
from modules import db
from threading import Timer
import time
from threading import Thread

MAINURL = "https://anthrmanga.anthrline.repl.co"
handle_content= Blueprint('handle_content', __name__)


@handle_content.route('/<ID>')
def returntomain(ID):
	# db.getbook(book)
	# Thread(target=removebook(book)).start()

	#activeid = request.cookies.get('uuid')
	# if activeid != None:
	#user = db.isloggedin(activeid)
	# 	if user:
	# 		chapter = db.getchapterbyid(ID)

	# 		book = db.getbookbyid(chapter['book'])

	#print(activeid)
	#print(user) 

	return send_file(os.path.join('bibi-bookshelf/', ID))

@handle_content.route('/covers/<image>')
def coverhandler(image):
    return send_file(os.path.join('modules/covers', image))

def removebook(book):
	print("REMOVING")
	time.sleep(1)
	print("REMOVED")
