import re
from requests_html import HTMLSession, HTML
from datetime import datetime
import lxml

session = HTMLSession()

def gen_tweets(url, headers, count):
    r = session.get(url, headers=headers)
    while count > 0:
        html = HTML(html=r.json()['items_html'],
                    url='bunk', default_encoding='utf-8')
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
            yield tweet
        r = session.get(
            url, params = {'max_position': last_tweet}, headers = headers)

def get_tweets(search, type_, count):
    url1 = f'https://twitter.com/i/profiles/show/{search}/timeline/tweets'
    url2 = f'https://twitter.com/i/search/timeline?q=%23{search}'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    if type_ == 1:
        url = url1
    else:
        url = url2
    r = session.get(url, headers=headers)
    if r.status_code == 404:
        return 404
    try:
        html = HTML(html=r.json()['items_html'],
                    url='bunk', default_encoding='utf-8')
    except lxml.etree.ParserError:
        return []
    tweets = []
    for t in gen_tweets(url, headers, count):
        tweets.append(t)
    return tweets

