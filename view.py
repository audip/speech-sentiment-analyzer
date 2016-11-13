from pymongo import MongoClient
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    tot_pos, tot_neg = 1, 1
    hateDocuments = []
    if request.method == 'POST':
        searchTerm = request.form['searchBox']

        conn = MongoClient('mongodb://audip:audip@ds151917.mlab.com:51917')
        db = conn['speech-db']
        collection = db['hate_speech']
        hateDocuments = collection.find({"hate": "true"})
        documents = collection.find({"sentiment": {"$ne": "neutral"}})

        for doc in documents:
            if doc["sentiment"] == 'Positive':
                tot_pos += 1
            else:
                tot_neg += 1

    return render_template('index.html', hateTweets=hateDocuments, positive=(tot_pos/(tot_neg+tot_pos)), negative=(tot_neg/(tot_neg+tot_pos)))

if __name__ == '__main__':
    app.run(debug=True, port=5000)