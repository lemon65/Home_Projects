#!/usr/bin/python

# Simple script to scrape rss feeds and post data to a twitter account

# ---- Twitter Bot setup ----
# you need to add an app to your twitter account, and get the API keys
# add these keys to the "call_and_connect_twitter" function. 
# To Edit the run time run the command 'crontab -e'
# it will then pull rss data and post it to the connected twitter account.
# Questions ? send me an email @ schoettger.aaron@gmail.com




import sys
import time
import twitter
import random as rd
import feedparser
import urllib, urlparse, httplib


# Class to chop up URLs and make them smaller
class URLShortener:
    BITLY_AUTH = 'login=foo&apiKey=bar'
    services = {'api.bit.ly':"http://api.bit.ly/shorten?version=2.0.1&%s&format=text&longUrl=" % BITLY_AUTH,
                'api.tr.im':'/api/trim_simple?url=',
                'tinyurl.com': '/api-create.php?url=',
                'is.gd':'/api.php?longurl='}
    def query(self, url):
        for shortener in self.services.keys():
            c = httplib.HTTPConnection(shortener)
            c.request("GET", self.services[shortener] + urllib.quote(url))
            r = c.getresponse()
            shorturl = r.read().strip()
            if ("Error" not in shorturl) and ("http://" + urlparse.urlparse(shortener)[1] in shorturl):
                return shorturl
            else:
                continue
                raise IOError

# Scrape the given rss feed for the first three articles 
def data_gather(url_step, count):
    url_class = URLShortener()
    data_dict = {}
    data = feedparser.parse(url_step)
    raw_data = data.entries[count]
    head_line = raw_data.get('title')
    full_url = raw_data.get('link')
    tiny_url = url_class.query(full_url)
    data_dict[head_line] = tiny_url
    return data_dict


# Calling the twitter API and sending data to the account
def call_and_connect_twitter(payload):
    api = twitter.Api(consumer_key='',
            consumer_secret='',
            access_token_key='',
            access_token_secret='')
    api.PostUpdate(payload)
    return


# Quick Function to strip bad chars out of Text
def norm_data(input_string, target_bad_char, replace_with):
    bad_char_list = ['\n', '\t', target_bad_char]
    for char_step in bad_char_list:
        mod_input = input_string.replace(char_step, replace_with)
    return mod_input

# Main call to start the whole process off
def main():
    data_urls = ['http://www.gamespot.com/feeds/news/',
                 'http://feeds.videogamer.com/rss/allupdates.xml',
                 'http://feeds.feedburner.com/GamasutraNews',
                 'http://dynamic.feedsportal.com/pf/510578/http://www.pcgamer.com/feed/rss2/',
                 'http://n4g.com/rss/news?channel=pc&sort=latest',
                 'http://www.gamespot.com/feeds/mashup/',
                 'http://www.gamespot.com/feeds/reviews/',
                 'http://www.gameinformer.com/feeds/thefeedrss.aspx']
    ran_list_val = rd.randint(0, len(data_urls) - 1)
    count_rand = rd.randint(0, 6)
    data_dict = data_gather(data_urls[ran_list_val], count_rand)
    for data_k, data_v in data_dict.iteritems():
        data_k = norm_data(data_k, "'",'')
        data_v = norm_data(data_v, "'",'') + ' '
        payload = "%s -- %s %s" % (data_k, data_v, '#Gaming #gamers #gamenews')
        call_and_connect_twitter(payload)

if __name__ == "__main__":
    sys.exit(main())
