from pymongo import MongoClient
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    tot_pos, tot_neg = 0, 0
    hateTweets = []
    if request.method == 'POST':
        searchTerm = request.form['searchBox']

        if searchTerm != "" and request.form['submit'] == 'Search':
            db = MongoClient('mongodb://audip:audip@ds151917.mlab.com:51917/speech-db')
            collection = db.get_collection('hate_speech')
            documents = collection.find()

            for doc in documents:
                if doc["sentiment"] == 'Positive':
                    tot_pos += 1
                else:
                    tot_neg += 1

                if doc["hate"] == "true":
                    hateTweets.append(doc)

    return render_template('index.html', barGraph=hateTweets, positive=(tot_pos/(tot_neg+tot_pos)), negative=(tot_neg/(tot_neg+tot_pos)))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)