#!/usr/bin/env python
"""
Fetch the latest stories from lobste.rs and post them to twitter.
"""

import os
import sqlite3
import sys
import time

#import feedparser
import requests
#import twitter

AUTH = {'consumer': {'key': os.getenv("LB_TWITTER_CONSUMER_KEY"),
                     'secret': os.getenv("LB_TWITTER_CONSUMER_SECRET")},
        'access': {'token': os.getenv("LB_TWITTER_ACCESS_KEY"),
                   'secret': os.getenv("LB_TWITTER_ACCESS_SECRET")}}
FEED_URL = "https://lobste.rs/newest.rss"
DB_PATH = os.getenv('LB_DATABASE_PATH')
MAX_TITLE_LEN = 115
NUM_STORIES = 5
DELAY = 900                 # check every 15 minutes
DEKAY_STEP = 300            # report every 5 minutes

def ellipses(title):
    """
    If the title is longer than the allowed size, shorted it
    with ellipses.
    """
    if len(title) < MAX_TITLE_LEN:
        return title
    working_title = title[:MAX_TITLE_LEN]
    if working_title.endswith(' '):
        working_title.strip()
    else:
        space = working_title.rfind(' ')
        working_title = working_title[:space]
    return '%s...' % (working_title, )


def story_to_status(story):
    """
    Convert a story to a suitable twitter status.
    """
    return '%s (%s)' % (ellipses(story['title']), story['link'])


def fetch_stories():
    """
    Retrieve the latest stories from lobsters, limited to the latest
    NUM_STORIES stories.
    """
    req = requests.get(FEED_URL)
    stories = feedparser.parse(req.content)['entries'][:NUM_STORIES]

    return stories


def postedp(story):
    """
    Determine whether a story has already been psoted via the
    database.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('SELECT * from posted where link=?', (story['link'], ))
    if len(cur.fetchall()) > 0:
        return True
    else:
        return False


def mark_posted(story):
    """
    Update the database with story to mark it as read
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    values = (story['guid'], story['title'], story['link'])
    cur.execute('insert into posted values (?, ?, ?)', values)
    did_update = cur.rowcount > 0
    cur.close()
    conn.commit()
    return did_update

def twitter_auth():
    """
    Authenticate to Twitter and return an API object suitable for
    interacting with Twitter.
    """
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
    """
    Post the story to Twitter.
    """
    api = twitter_auth()
    if None == api:
        print '[!] twitter auth error!'
    else:
        status = api.PostUpdate(story_to_status(story))
        if not status:
            print '[!] error posting story!'
        else:
            print '[+] posted %s' % (story_to_status(story))
            return mark_posted(story)


def update():
    """
    Fetch the latest stories, posting those that haven't been
    posted yet.
    """
    for story in fetch_stories()[::-1]: # post earlier stories first
        print '[+] story link: %s' % (story['link'], ),
        if not postedp(story):
            if post_story(story):
                print ' posted'
            else:
                print ' error posting!'
        else:
            print ' skipping'


def main():
    """
    The run loop: every DELAY seconds, run the update function to
    check for and possibly post new stories.
    """
    while True:
        update()
        for delay in range(0, DELAY, DELAY_STEP):
            remaining = DELAY - delay
            print '[+] sleeping for another %d seconds' % (remaining, )
            time.sleep(DELAY_STEP)

if '__main__' == __name__:
    print '[+] starting lobsterpie'
    main()
