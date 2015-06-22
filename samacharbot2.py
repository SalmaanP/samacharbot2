# -*- coding: utf-8 -*-
__author__ = 'salmaan'

import sys
from goose import Goose
import praw
import smrzr
from altsummary import summary

blocked = {"youtube.com", "imgur.com", "i.imgur.com", "imgflip.com", "flipkart.com", "snapdeal.com", "ebay.com", "blogs.wsj.com", "pbs.twimg.com", "twitter.com", "buzzfeed.com","ptinews.com", "vine.co", "indigogo.com", "en.wikipedia.com", "self.india", "niticentral.com", "nytimes.com"}
blockedid = {}

r = praw.Reddit(user_agent='test for bot')
#implement oauth soon
r.login('uname', 'pass')

subreddit = r.get_subreddit('TESTBOTTEST')
submissions = subreddit.get_hot(limit=100)

for submission in submissions:
    print submission.title
    upvotes = 1
    if upvotes > 0:
        if submission.domain not in blocked and submission.id not in blockedid:
            try:
                link = submission.url
                summ_article = smrzr.Summarizer(link)
                keypoints = summ_article.keypoints
                try:
                    submission.add_comment(keypoints)
                except Exception as e:
                    print "Unknown ERROR\n"
                    print type(e)
                    print e.args
                    print e
                    print submission.id
                    print "\n"
                    continue

                print "Done normally"

            except smrzr.ArticleExtractionFail as a:
                print "Article Extraction Failed"
                continue

            except AssertionError as b:
                print "Assertion Error"
                g = Goose()
                try:
                    summ_article = article = g.extract(url=link)
                except Exception as e:
                    print "Unknown ERROR\n"
                    print type(e)
                    print e.args
                    print e
                    print submission.id
                    print "\n"
                    continue
                continue
                text = summ_article.cleaned_text
                keypoints = summary(text)
                try:
                    submission.add_comment(keypoints)
                except Exception as e:
                    print "Unknown ERROR\n"
                    print type(e)
                    print e.args
                    print e
                    print submission.id
                    print "\n"
                    continue
                continue

            except Exception as e:
                print "Unknown ERROR"
                print type(e)
                print e.args
                print e
                print submission.id
                print "\n"
                continue

# link="http://www.newindianexpress.com/nation/Man-Caught-Urinating-in-Delhi-Metro-Disturbed-Passenger-Uploads-Video-in-Social-Media/2015/06/21/article2878562.ece"
# summ_article = smrzr.Summarizer(link)
# summaryy = summ_article.summary
# print summaryy.encode("utf=8")
