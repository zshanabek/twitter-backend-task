# Introduction
This API provides data about tweets. Get tweets searching by user or hashtag.  
You can read documentation for API [here...](https://documenter.getpostman.com/view/1700393/RWgjZ2DU)
# Installation

1. Clone repository
```bash
$ git clone https://github.com/zshanabek/zhunisali-project
$ cd zhunisali-project
```
2. Install dependencies
```bash
$ pip install -r requirements.txt
```
3. Run server
```bash
$ python3 start.py
```
4. Get tweets
```bash
$ curl localhost:5000/users/zshanabek
```
```json
{
  "tweets": [
    {
      "account": {
        "fullname": "Zhunisali Shanabek", 
        "href": "/zshanabek", 
        "id": "760766794940416000"
      }, 
      "date": "Fri, 28 Sep 2018 15:26:04 GMT", 
      "hashtags": [
        "#postmanclient"
      ], 
      "likes": 213, 
      "replies": 54, 
      "retweets": 42, 
      "text": "If you need to document your API, use @postmanclient. Excellent software.\n#postmanclient"
    }, 
  ]
}
```

# Overview
You can set the limit of tweets in response by typing argument: `limit`.  
For example. `localhost:5000/users/zshanabek?limit=10`.  
Default is 30.

Only Python 3.6+ is supported
