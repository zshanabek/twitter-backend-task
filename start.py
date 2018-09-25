from twitter_scraper import get_tweets
import pprint
from flask import Flask, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

tweets = []


for tweet in get_tweets('zshanabek', pages=1):
	tweets.append({
		'date': tweet['time'],
		'likes': tweet['likes'],
		'replies': tweet['replies'],
		'retweets': tweet['retweets'],
		'text': tweet['text']
	})


@app.route('/test/api/v1.0/tweets', methods=['GET'])
def get_tasks():
    return jsonify({'tweets': tweets})

if __name__ == '__main__':
    app.run(debug=True)