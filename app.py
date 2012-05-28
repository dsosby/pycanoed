import os
import pymongo
from flask import Flask, g, render_template

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def get_db():
    db_url  = app.config['DATABASE_URL']
    db_name = pymongo.uri_parser.parse_uri(db_url)['database']
    if db_name != None:
        return (pymongo.Connection(db_url),db_name)
    return (None,None)

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
def hello():
    count = "?"
    if g.db:
        count = g.db.posts.count()
        posts = [dict(timestamp=post["timestamp"], entry=post["entry"]) for post in g.db.posts.find()]
    return render_template('common.html', count=count, posts=posts)

@app.route('/about')
def about():
    return "About!"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
