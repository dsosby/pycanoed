import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return r"ipyCanoed<br/>{}".format(mongourl)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    #mongourl = os.environ.get('MONGOHQ_URL', "No URL")
    app.run(host='0.0.0.0',port=port)
