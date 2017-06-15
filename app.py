#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "news.search":
        return {}
    baseurl = "https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=60969da0a38e4cf1aad619158c413030"
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


#def makeYqlQuery(req):
    #result = req.get("result")
    #parameters = result.get("parameters")
    #news = parameters.get("news.search")
    #if news is None:
        #return None

def makeWebhookResult(res):
    articles = res.get('articles')
    if articles is None:
        return {}

    author = articles.get('author')
    if author is None:
        return {}

    title = articles.get('title')
    if title is None:
        return {}

    description= articles.get('description')
    url = articles.get('url')
    #units = channel.get('units')
    
    #condition = item.get('condition')
    #if condition is None:
       # return {}

    print(json.dumps(item, indent=4))

    speech = "latest news" +author.get()+""+title.get()+""+description.get()+""+url.get()

    #print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-news-search"
    }
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
