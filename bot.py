#!/usr/bin/env python

import os
import sqlite3
import sys
import time

import feedparser
import requests
import twitter

AUTH = {'consumer': {'key': os.getenv("LB_TWITTER_CONSUMER_KEY"),
                     'secret': os.getenv("LB_TWITTER_CONSUMER_SECRET")},
        'access': {'token': os.getenv("LB_TWITTER_ACCESS_KEY"),
                   'secret': os.getenv("LB_TWITTER_ACCESS_SECRET")}}

FEED_URL = "https://lobste.rs/newest.rss"
DB_PATH = os.getenv('LB_DATABASE_PATH')
MAX_TITLE_LEN = 115

def ellipses(title):
    if len(title) < MAX_TITLE_LEN:
        return title
    else:
        return '%s...' % (title, )

def mkstory(story):
    return {'title': ellipses(story['title']),
            'guid': story['guid'],
            'link': story['link']}

def disp_story(story):
    print '%s (%s) comments: %s' % (story['title'],
                                    story['link'],
                                    story['guid'])

def story_to_status(story):
    return '%s (%s)' % (ellipses(story['title']), story['link'])

def fetch_stories():
    req = requests.get(FEED_URL)
    stories = feedparser.parse(req.content)['entries'][:5]

    return stories

def postedp(story):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('SELECT * from posted where link=?', (story['link'], ))
    if len(cur.fetchall()) > 0:
        return True
    else:
        return False

def mark_posted(story):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    values = (story['guid'], story['title'], story['link'])
    cur.execute('insert into posted values (?, ?, ?)', values)
    cur.close()
    conn.commit()

def twitter_auth():
    try:
        api = twitter.Api(consumer_key=AUTH['consumer']['key'],
                          consumer_secret=AUTH['consumer']['secret'],
                          access_token_key=AUTH['access']['token'],
                          access_token_secret=AUTH['access']['secret'])
    except twitter.TwitterHTTPError as error:
        print '[!] exception authentication to twitter: %s' % (error, )
        return None
    if not api.VerifyCredentials():
        return None
    return api

def post_story(story):
    api = twitter_auth()
    if None == api:
        print '[!] twitter auth error!'
    else:
        status = api.PostUpdate(story_to_status(story))
        if not status:
            print '[!] error posting story!'
        else:
            print '[+] posted %s' % (story_to_status(story))
            mark_posted(story)

def update():
    for story in fetch_stories():
        if not postedp(story):
            post_story(story)
        else:
            print '[+] skipping %s' % (story['link'], )

def main():
    while True:
        update()
        time.sleep(900)

if '__main__' == __name__:
    main()
