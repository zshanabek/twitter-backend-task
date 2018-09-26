#!senv/bin/python
from twitter_scraper import get_tweets, get_tweets_by_hashtag
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/users/<string:username>', methods=['GET'])
def index(username):
	args = request.args
	try:
		count = int(args['limit'])
		tweets = get_tweets(username, count)
	except KeyError:
		tweets = get_tweets(username)
	return jsonify({'tweets': tweets})

@app.route('/hashtags/<string:hashtag>', methods=['GET'])
def get_by_hashtags(hashtag):
	args = request.args
	try:
		count = int(args['limit'])
		tweets = get_tweets_by_hashtag(hashtag, count)
	except KeyError:
		tweets = get_tweets_by_hashtag(hashtag)
	return jsonify({'tweets': tweets})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)