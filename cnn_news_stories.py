#!/usr/bin/python

#   _______  _____________      __  _________           __________ ___________________
#   \      \ \_   _____/  \    /  \/   _____/           \______   \\_____  \__    ___/
#   /   |   \ |    __)_\   \/\/   /\_____  \    ______   |    |  _/ /   |   \|    |   
#  /    |    \|        \\        / /        \  /_____/   |    |   \/    |    \    |   
#  \____|__  /_______  / \__/\  / /_______  /            |______  /\_______  /____|   
#          \/        \/       \/          \/                    \/         \/         

# Simple script to poll the top stories on CNN.rss and send them to a cell phone
# To Edit the run time run the command 'crontab -e'

# Steps to use -- > 
# - update the log path
# - add a phone num and provider
# - Start a local smtp server, with an account (use googles SMTP server)
# - install mutt
# - Setup when the data will be sent to your phone

import os 
import sys
import time
import feedparser
import logging as log
import urllib, urlparse, httplib

NOW = time.strftime("%m-%d-%Y", time.gmtime())
# TODO -- correct path for your system..
local_log_file = '/home/lemon65/projects/python_scripts/news_script/logs/%s_news.log' % NOW

# Add more users here that would like the News update
#############################################
# TODO -- Update the target address ...
target_addrs = ['PHONE_NUM_HERE@txt.att.net']
#############################################

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
def data_gather(url_step):
    url_class = URLShortener()
    data_dict = {}
    count = 1
    while count <= 3:
        data = feedparser.parse(url_step)
        raw_data = data.entries[count]
        head_line = raw_data.get('title')
        full_url = raw_data.get('link')
        tiny_url = url_class.query(full_url)
        data_dict[head_line] = tiny_url
        count += 1
    return data_dict

# Function to use the local smtp server to send the mail
def simple_mail(rss_name, file_loc, target_addr):
    log.info('Seanding Mail, To: %s, Subject:%s, File: %s' % (target_addr, rss_name, file_loc))
    os.system('mutt -s "%s" %s < %s' % (rss_name, target_addr, file_loc))
    return

# Quick Function to strip bad chars out of Text
def norm_data(input_string, target_bad_char, replace_with):
    bad_char_list = ['\n', '\t', target_bad_char]
    for char_step in bad_char_list:
        mod_input = input_string.replace(char_step, replace_with)
    return mod_input

# Main call to start the whole process off
def main():
    FORMAT = '%(asctime)-15s | %(message)s'
    log.basicConfig(format=FORMAT, filename=local_log_file, level=log.INFO)
    data_urls = ['http://rss.cnn.com/rss/cnn_topstories.rss',
                 'http://rss.cnn.com/rss/cnn_world.rss']
    for url_step in data_urls:
        rss_name = url_step.split('/')[-1].strip('.rss')
        file_loc = './%s_tmp_storage_before_send.txt' % rss_name
        data_dict = data_gather(url_step)
        open_file = open(file_loc, 'w')
        for data_k, data_v in data_dict.iteritems():
            data_k = norm_data(data_k, "'",'')
            data_v = norm_data(data_v, "'",'') + ' '
            log.info("Adding: %s - %s" % (data_k, data_v))
            open_file.write(data_k + ' -- ' + data_v + '\n')
        open_file.close()
        for address_step in target_addrs:
            simple_mail(rss_name, file_loc, address_step)
            time.sleep(10)
            os.system('rm %s' % file_loc)

if __name__ == "__main__":
    sys.exit(main())
