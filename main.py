from blueprints.sessions import sessions
from blueprints.manga import manga
from blueprints.feed import feed
from blueprints.handle_content import handle_content
from blueprints.controls import controls
from flask import (
    Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)

app = Flask('app')

app.register_blueprint(sessions, url_prefix='/sessions')
app.register_blueprint(manga, url_prefix='/manga')
app.register_blueprint(feed, url_prefix='/feed')
app.register_blueprint(handle_content, url_prefix='/bibi-bookshelf')
app.register_blueprint(controls, url_prefix='/controls')

@app.route('/')
def main():
  return redirect('/feed')


app.config.update(TEMPLATE_AUTO_RELOAD=True)
app.config.update()
app.config['UPLOAD_FOLDER'] = './modules/covers'
#app.run()