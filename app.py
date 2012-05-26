import os
import pymongo
from flask import Flask, g

DATABASE = os.environ.get('MONGOHQ_URL', 'mongodb://guest:pass@localhost:27017/pycanoed')
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def get_db():
    return pymongo.Connection(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def hello():
    return r"pyCanoed<br/>DB is {} with databases {}".format(g.db, g.db.database_names())

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0',port=port)
