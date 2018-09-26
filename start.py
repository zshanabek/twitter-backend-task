#!senv/bin/python
from twitter_scraper import get_tweets
import pprint
from flask import Flask, jsonify, abort, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False



def	get_tweets_by_username(username):
	tweets = []
	for tweet in get_tweets(username, pages=1):
		tweets.append({
			'date': tweet['time'],
			'likes': tweet['likes'],
			'replies': tweet['replies'],
			'retweets': tweet['retweets'],
			'text': tweet['text']
		})
	return tweets


@app.route('/users/<string:username>', methods=['GET'])
def get_task(username):
	tweets = get_tweets_by_username(username)
	return jsonify({'tweets': tweets})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)