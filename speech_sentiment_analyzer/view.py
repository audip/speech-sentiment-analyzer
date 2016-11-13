from pymongo import MongoClient
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def renderHome():
    if request.method == 'POST':
        searchTerm = request.form['searchBox']
        tot_pos, tot_neg = 0,0

        if searchTerm != "" and request.form['submit'] == 'Search':
            db = MongoClient('mongodb://audip:audip@ds151917.mlab.com:51917/speech-db')
            collection = db.get_collection('hate_speech')

            documents = collection.find()
            for doc in documents:
                if doc.sentiment == 'Positive':
                    tot_pos += 1
                else:
                    tot_neg += 1