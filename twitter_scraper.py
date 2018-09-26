import re
from requests_html import HTMLSession, HTML
from datetime import datetime

session = HTMLSession()
def gen_tweets(url, headers, count):
    r = session.get(url, headers=headers)
    while count > 0:
        try:
            html = HTML(html=r.json()['items_html'],
                        url='bunk', default_encoding='utf-8')
        except KeyError:
            raise ValueError(
                f'Oops! Either user does not exist or is private.')

        comma = ","
        dot = "."
        tweets = []
        for tweet in html.find('.stream-item'):
            if count == 0:
                break
            user_id = tweet.find(".account-group")[0].attrs['data-user-id']
            href = tweet.find(".account-group")[0].attrs['href']
            full_name = tweet.find('.fullname')[0].full_text 
            text = tweet.find('.tweet-text')[0].full_text
            time = datetime.fromtimestamp(
                int(tweet.find('._timestamp')[0].attrs['data-time-ms'])/1000.0)
            interactions = [x.text for x in tweet.find(
                '.ProfileTweet-actionCount')]
            replies = int(interactions[0].split(" ")[0].replace(comma, "").replace(dot,""))
            retweets = int(interactions[1].split(" ")[
                            0].replace(comma, "").replace(dot,""))
            likes = int(interactions[2].split(" ")[0].replace(comma, "").replace(dot,""))
            hashtags = [hashtag_node.full_text for hashtag_node in tweet.find('.twitter-hashtag')]
            tweets.append({
                'account': {
                    'fullname': full_name,
                    'href': href,
                    'id': user_id
                },
                'date': time,
                'hashtags': hashtags,
                'likes': likes,
                'replies': replies, 
                'retweets': retweets,
                'text': text
            })
            count -= 1                
        last_tweet = html.find('.stream-item')[-1].attrs['data-item-id']

        for tweet in tweets:
            if tweet:
                tweet['text'] = re.sub('http', ' http', tweet['text'], 1)
                yield tweet

        r = session.get(
            url, params = {'max_position': last_tweet}, headers = headers)
    return tweets

def get_tweets(user, count=30):
    url = f'https://twitter.com/i/profiles/show/{user}/timeline/tweets'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'
    }
    tweets = []
    for tweet in gen_tweets(url, headers, count):
        tweets.append(tweet)
    return tweets

def get_tweets_by_hashtag(hashtag, count=30):
    url = f'https://twitter.com/i/search/timeline?q=%23{hashtag}'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8'
    }
    tweets = []
    for tweet in gen_tweets(url, headers, count):
        tweets.append(tweet)
    return tweets
