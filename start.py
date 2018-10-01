#!senv/bin/python
from twitter_scraper import get_tweets
from flask import Flask, jsonify, make_response, request, abort

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/users/<string:username>', methods=['GET'])
def index(username):
	args = request.args
	try:
		count = int(args['limit'])
	except:
		count = 30
	tweets = []
	for tweet in get_tweets(username, 1, count):
		if tweet == 404:
			abort(404)
		tweets.append(tweet)
	return jsonify({'tweets': tweets})

@app.route('/hashtags/<string:hashtag>', methods=['GET'])
def get_by_hashtags(hashtag):
	args = request.args
	try:
		count = int(args['limit'])
	except:
		count = 30
	tweets = []
	for tweet in get_tweets(hashtag, 2, count):
		tweets.append(tweet)
	return jsonify({'tweets': tweets})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
