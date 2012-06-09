import datetime
import hashlib
import os
import pymongo
from flask import Flask, g, render_template, request, jsonify, \
        flash, redirect, url_for

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def get_db():
    db_url  = app.config['DATABASE_URL']
    db_name = pymongo.uri_parser.parse_uri(db_url)['database']
    if db_name != None:
        return (pymongo.Connection(db_url),db_name)
    return (None,None)

def get_header_info():
    count = g.db.posts.count() if g.db else '?'
    links = []
    if request.path != '/about':
        links.append('about')
    if request.path != '/':
        links.append('index')
    links.append('post')
    return dict(count=count, links=links)

@app.before_request
def before_request():
    g.dbconn, db_name = get_db()
    if g.dbconn and db_name:
        g.db = g.dbconn[db_name]
    else:
        g.db = None

@app.teardown_request
def teardown_request(exception):
    if g.db:
        g.dbconn.disconnect()

@app.route('/')
def index():
    if g.db:
        posts = [post for post in g.db.posts.find()]
    return render_template('index.html', header=get_header_info(), posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', header=get_header_info())

@app.route('/post', methods=['POST','GET'])
def post():
    if request.method == 'POST':
        if verify_password(request.values.get('password', type=str)):
            title = request.values.get('title', "I Canoed!", type=str)
            entry = request.values.get('entry', "...but I didn't care enough to write about it.", type=str)
            if add_entry(title, entry):
                return redirect(url_for('index'))
            else:
                flash("Error inserting")
        else:
            flash("Incorrect Password")

    return render_template('post.html', header=get_header_info())

@app.route('/verify')
def verify():
    arg_pass  = request.args.get("password", type=str)
    return jsonify(valid=verify_password(arg_pass))

def verify_password(password):
    """Returns true if the password is acceptable"""
    hash_pass = hashlib.sha1(password + app.config['SECRET_KEY']).hexdigest()
    valid     = hash_pass == app.config['VALID_PASSWORD']
    return valid

def add_entry(title, entry, timestamp=None):
    added = False
    if g.db:
        if not timestamp:
            timestamp = datetime.datetime.now()
        g.db.posts.insert(dict(title=title, entry=entry, timestamp=timestamp))
        added = True

    return added

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
