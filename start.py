#!senv/bin/python
from twitter_scraper import get_tweets
import pprint
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def	get_tweets_by_username(username, count=30):
	tweets = []
	for tweet in get_tweets(username, count):
		tweets.append({
			'date': tweet['time'],
			'hashtags': tweet['entries']['hashtags'],
			'likes': tweet['likes'],
			'replies': tweet['replies'],
			'retweets': tweet['retweets'],
			'text': tweet['text']
		})
	return tweets

@app.route('/users/<string:username>', methods=['GET'])
def get_task(username):
	args = request.args
	try:
		count = int(args['limit'])
		tweets = get_tweets_by_username(username, count)
	except KeyError:
		tweets = get_tweets_by_username(username)
	print ('len of list:=================' + str(len(tweets)))
	return jsonify({'tweets': tweets})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)