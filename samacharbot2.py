# -*- coding: utf-8 -*-
__author__ = 'salmaan'

from goose import Goose
import praw
import smrzr
from altsummary import summary
import os

blocked = {"youtube.com", "imgur.com", "i.imgur.com", "imgflip.com", "flipkart.com", "snapdeal.com", "ebay.com",
           "blogs.wsj.com", "pbs.twimg.com", "twitter.com", "buzzfeed.com", "ptinews.com", "vine.co", "indigogo.com",
           "en.wikipedia.com", "self.india", "niticentral.com", "nytimes.com","youtu.be","saddahaq.com"}
blockedid = []

uname=os.environ['uname']
pwd=os.environ['pass']
r = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
# implement oauth soon
r.login("uname", "pass")

subreddit = r.get_subreddit('india+TESTBOTTEST')

while True:

    fo = open("looked.txt", "a+")
    fo.seek(0, 0)
    position = fo.tell()
    str1 = fo.read()
    fo.seek(position)

    submissions = subreddit.get_new(limit=3)
    for submission in submissions:
        print submission.title.encode('ascii','replace')
        summ = ""
        endmsg = """^I'm ^a ^bot ^| ^OP ^can ^reply ^with ^"delete" ^to ^remove ^| [^Message ^Creator](http://www.reddit.com/message/compose/?to=sallurocks) ^| [^Source](https://github.com/hunkdivine/samacharbot2)"""
        br = "\n\n---\n\n"
        upvotes = int(submission.score)
        if upvotes > 0:
            if submission.domain not in blocked and submission.id not in str1:
                try:
                    fo.write(submission.id+" ")
                    link = submission.url
                    summ_article = smrzr.Summarizer(link)
                    keypoints = summ_article.keypoints
                    summ = summ_article.summary
                    message = "\n\n> * ".join(keypoints)
                    message = "> * " + message

                    if len(message) > 100:
                        try:
                            submission.add_comment(summ + br + message.encode('ascii', 'replace') + br + endmsg)
                        except Exception as e:
                            print "1Unknown ERROR\n"
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
                        link = submission.url
                        article = g.extract(url=link)

                    except Exception as e:
                        print "2Unknown ERROR\n"
                        print type(e)
                        print e.args
                        print e
                        print submission.id
                        print "\n"
                        continue

                    text = article.cleaned_text
                    keypoints = summary(text)
                    title = article.title

                    if len(keypoints) > 100:
                        try:
                            # print keypoints
                            submission.add_comment(title + br + str(keypoints).encode('ascii', 'replace') + br + endmsg)

                        except Exception as e:
                            print "3Unknown ERROR\n"
                            print type(e)
                            print e.args
                            print e
                            print submission.id
                            print "\n"
                            continue
                    continue

                except Exception as e:
                    print "4Unknown ERROR"
                    print type(e)
                    print e.args
                    print e
                    print submission.id
                    print "\n"
                    continue

            else:
                print "Id blocked or domain blocked"

                unread = r.get_unread(limit=None)
                print "here"
                for msg in unread:
                    print msg.body
                    if msg.body.lower() == 'delete':
                        try:
                            print "found one"
                            idd = msg.id
                            idd = 't1_' + idd
                            print idd
                            comment = r.get_info(thing_id=idd)
                            parentid = comment.parent_id
                            print parentid
                            comment_parent = r.get_info(thing_id=parentid)
                            sublink = comment_parent.link_id
                            author1 = r.get_info(thing_id=sublink)
                            print author1.author
                            print msg.author.name
                            if (str(msg.author.name) == str(author1.author)):
                                comment_parent.delete()
                                print "deletedd"

                                msg.mark_as_read()
                            else:

                                msg.mark_as_read()
                            continue
                        except Exception as e:
                            print "5Unknown ERROR"
                            print type(e)
                            print e.args
                            print e
                            print "\n"
                            # continue
                            msg.mark_as_read()
                            continue
                continue
