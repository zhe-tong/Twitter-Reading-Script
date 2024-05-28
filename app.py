from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route('/tweets')
def get_tweets():
    conn = sqlite3.connect('elon_musk_tweets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tweets")
    tweets = c.fetchall()
    conn.close()
    return jsonify(tweets)

if __name__ == '__main__':
    app.run(debug=True)
