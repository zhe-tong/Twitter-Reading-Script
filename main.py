import tweepy
import sqlite3
from config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from datetime import datetime, timedelta

# Connect to Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Connect to SQLite database
conn = sqlite3.connect('elon_musk_tweets.db')
c = conn.cursor()

# Create tweets table (if not exists)
c.execute('''CREATE TABLE IF NOT EXISTS tweets
             (id INTEGER PRIMARY KEY, tweet_id TEXT UNIQUE, content TEXT, created_at TEXT)''')

# Fetch and insert historical tweets
def fetch_and_store_historical_tweets():
    end_time = datetime.utcnow()  # Current time
    start_time = end_time - timedelta(days=7)  # One week ago
    tweets = api.user_timeline(screen_name='elonmusk', tweet_mode='extended', start_time=start_time,
                               end_time=end_time, max_results=200)
    for tweet in tweets:
        tweet_id = tweet.id_str
        content = tweet.full_text
        created_at = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')
        c.execute("INSERT OR IGNORE INTO tweets (tweet_id, content, created_at) VALUES (?, ?, ?)",
                  (tweet_id, content, created_at))
        print("Historical tweet inserted:", content)
    conn.commit()

fetch_and_store_historical_tweets()

# Query and print all tweets
c.execute("SELECT * FROM tweets")
rows = c.fetchall()
for row in rows:
    print(row)

# Close database connection
conn.close()
