__author__ = 'salmaan'
import praw
from prawoauth2 import PrawOAuth2Mini
import config


blocked = {"youtube.com", "imgur.com", "i.imgur.com", "imgflip.com", "flipkart.com", "snapdeal.com", "ebay.com",
           "blogs.wsj.com", "pbs.twimg.com", "twitter.com", "buzzfeed.com", "ptinews.com", "vine.co",
           "indigogo.com",
           "en.wikipedia.com", "self.india", "niticentral.com", "nytimes.com", "youtu.be", "saddahaq.com",
           "m.youtube.com", "docs.google.com"}

blockedid = []


def configstuff():

    uname = os.environ['uname']
    pwd = os.environ['pass']
    reddit_client = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
    oauth_helper = PrawOAuth2Mini(reddit_client, app_key=config.app_key,
                                  app_secret=config.app_secret,
                                  access_token=config.access_token,
                                  refresh_token=config.refresh_token, scopes=config.scopes)


def get_latest_posts():

    subreddit = r.get_subreddit('india+TESTBOTTEST')
    submissions = subreddit.get_new(limit=25)