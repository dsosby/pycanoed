import hashlib
import os
import pymongo
from flask import Flask, g, render_template, request, jsonify

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

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db') and g.db != None:
        g.dbconn.disconnect()

@app.route('/')
def index():
    if g.db:
        posts = [dict(timestamp=post["timestamp"], entry=post["entry"]) for post in g.db.posts.find()]
    return render_template('index.html', header=get_header_info(), posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', header=get_header_info())

@app.route('/post')
def post():
    return render_template('post.html', header=get_header_info())

@app.route('/verify')
def verify():
    arg_pass  = request.args.get("password", type=str)
    hash_pass = hashlib.sha1(arg_pass+ app.config['SECRET_KEY']).hexdigest()
    valid     = hash_pass == app.config['VALID_PASSWORD']
    return jsonify(valid=valid)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
