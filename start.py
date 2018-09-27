#!senv/bin/python
from twitter_scraper import get_tweets
from flask import Flask, jsonify, make_response, request, abort
import pdb

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/users/<string:username>', methods=['GET'])
def index(username):
	args = request.args
	try:
		count = int(args['limit'])
	except:
		count = 30
	tweets = get_tweets(username, 1, count)
	if tweets == 404:
		abort(404)
	else:
		return jsonify({'tweets': tweets})

@app.route('/hashtags/<string:hashtag>', methods=['GET'])
def get_by_hashtags(hashtag):
	args = request.args
	try:
		count = int(args['limit'])
	except:
		count = 30
	tweets = get_tweets(hashtag, 2, count)	
	return jsonify({'tweets': tweets})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)