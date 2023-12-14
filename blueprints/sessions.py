from flask import *
from modules import db

MAINURL = "/feed"
sessions = Blueprint('sessions', __name__)

@sessions.route('/')
def returntomain():
	return redirect(MAINURL)


# Forms
@sessions.route('/loginform')
def loginform():
	return render_template('loginform.html')

@sessions.route('/signupform')
def signupform():
	return render_template('signupform.html')

@sessions.route('/resetpasswordform')
def resetpasswordform():
	return render_template('resetpasswordform.html')

# Internal use
@sessions.route('/login', methods = ['POST','GET']) 
def login():
    print('ENTERING LOGIN')
    mail = request.form['mail']
    print('GOT MAIL')
    password = request.form['password']
    print('GOT PASSWORD')
    user = db.getlogininfo(mail, password)
    print(user)
    if user != False:
        resp = make_response(redirect(MAINURL))
        resp.set_cookie('uuid', user["activeid"], path='/')
        print('setting cookie')
        return resp
    else:
        print('IS NOT USER')
        return(loginform())

@sessions.route('/signup', methods = ['POST','GET'])
def signup():
	mail = request.form['mail']
	pswd = request.form['password']
	user = db.newuser(pswd, mail)

	resp = make_response(redirect(MAINURL))
	resp.set_cookie('uuid', user, samesite="None", path='/')
	return resp

@sessions.route('/resetpassword', methods = ['POST', 'GET'])
def resetpassword():
	mail = request.form['mail']
	pyrebasef.resetpassword(mail)
	return ('200')

@sessions.route('/logout')
def logout():
	activeid = request.cookies.get('uuid')
	resp = make_response(redirect(MAINURL))
	resp.set_cookie('uuid', '', expires=0, samesite="Strict")
	db.logout(activeid)
	return resp
