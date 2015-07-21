# -*- coding: utf-8 -*-
__author__ = 'salmaan'

from goose import Goose
import praw
import smrzr
from altsummary import summary
import os
import find_other_news_sources
import itertools
from prawoauth2 import PrawOAuth2Mini
import blacklist

blockedid = []

# Config Stuff

# uname = os.environ['uname']
# pwd = os.environ['pass']
r = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
# implement oauth soon ---done
# r.login(uname, pwd)
scopes = {u'edit', u'submit', u'read', u'privatemessages', u'identity', u'history'}
oauth_helper = PrawOAuth2Mini(r, app_key=os.environ['app_key'],
                              app_secret=os.environ['app_secret'],
                              access_token=os.environ['access_token'],
                              refresh_token=os.environ['refresh_token'], scopes=scopes)

subreddit = r.get_subreddit('india+TESTBOTTEST')

while True:

    # File to keep track of posts already looked, gets refreshed if bot is restarted.
    # put pointer at start, then reads the file to string and then puts the pointer back at the end.

    fo = open("looked.txt", "a+")
    fo.seek(0, 0)
    position = fo.tell()
    str1 = fo.read()
    fo.seek(position)

    # get new submissions and go through them.

    submissions = subreddit.get_new(limit=25)
    for submission in submissions:

        # Refresh auth token. expires 60 min.
        oauth_helper.refresh()

        # variable to keep track of cases where bot is restarted and file doesnt have previous submission data.
        visited = False

        #print submission.title.encode('ascii', 'replace')

        # message templates for 1st summary method
        summ = ""
        endmsg = """^I'm ^a ^bot ^| ^OP ^can ^reply ^with ^"delete" ^to ^remove ^| [^Message ^Creator](http://www.reddit.com/message/compose/?to=sallurocks) ^| [^Source](https://github.com/hunkdivine/samacharbot2) ^|"""
        help = " ^See ^how ^you ^can ^help! ^Visit ^the ^source ^and ^check ^out ^the ^Readme"
        endmsg = endmsg + help
        relevant_message = "\n\nHere are some relevant links for your viewing pleasure:^credits ^to ^u-sr33"
        br = "\n\n---\n\n"

        # if want to implement score based posts in future
        upvotes = int(submission.score)

        if upvotes > 0:

            # check if post not blocked by domain or already looked
            if submission.domain not in blacklist.blocked and submission.id not in str1:
                try:
                    # write submission  id to file to not post again
                    fo.write(submission.id + " ")

                    # check again if comment is already posted by bot and flip visited variable
                    try:
                        forest_comments = submission.comments
                    except Exception as e:
                        continue

                    for comment in forest_comments:
                        if str(comment.author) == 'samacharbot2':
                            #print "Went inside"
                            visited = True

                    # skip post if posted already
                    if visited == True:
                        continue

                    # get post information and summary using Smrzr. Format properly.
                    link = submission.url
                    summ_article = smrzr.Summarizer(link)
                    keypoints = summ_article.keypoints
                    summ = summ_article.summary
                    message = "\n\n> * ".join(keypoints)
                    message = "> * " + message
                    message = message.replace("`", "")
                    message = message.replace("#", "\#")

                    # Find relevant links using google
                    relevant_list = find_other_news_sources.find_other_news_sources(url=link)

                    # check if its null or doesnt contain anything.
                    if relevant_list is None or len(relevant_list) == 0:
                        if len(message) > 100:
                            try:
                                # print keypoints
                                submission.add_comment(summ + br + message.encode('ascii', 'replace') + br + endmsg)
                                continue

                            except Exception as e:
                                print "3Unknown ERROR\n"
                                print type(e)
                                print e.args
                                print e
                                print submission.id
                                print "\n"
                                continue
                    else:

                        # otherwise get title and url and append to message.
                        relevant_title = []
                        relevant_link = []

                        # temp variable to see if new link isn't same as last one.
                        temp_alink = ""
                        temp_blink = ""
                        for a_link in relevant_list:
                            relevant_title.append(a_link[0])
                            relevant_link.append(a_link[1])

                        for (a_link, b_link) in itertools.izip(relevant_title, relevant_link):

                            # if no title found, name the link.
                            if a_link is None:
                                a_link = "This"
                            if b_link is None or b_link == link:
                                continue
                            if temp_blink == b_link:
                                continue
                            try:
                                print "inside normal"
                                relevant_message = relevant_message + "\n\n" + "> * " + "[" + a_link + "]" + "(" + b_link + ")"
                                temp_alink = a_link
                                temp_blink = b_link
                            except Exception as e:
                                print e


                                #relevant_message = relevant_message + "---"

                    # post comment if summary is substantial
                    if len(message) > 150:
                        try:
                            submission.add_comment(
                                summ + br + message.encode('ascii', 'replace') + br + relevant_message + br + endmsg)
                        except Exception as e:
                            print "1Unknown ERROR\n"
                            print type(e)
                            print e.args
                            print e
                            print submission.id
                            print "\n"
                            continue

                            #print "Done normally"

                except smrzr.ArticleExtractionFail as a:
                    print "Article Extraction Failed"
                    continue

                # in case Smrzr fails to get summary, try another method
                except AssertionError as b:
                    print "Assertion Error"

                    # get url and text from link
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
                    keypoints = keypoints.replace("`", "")
                    keypoints = keypoints.replace("#", "\#")

                    # same old relevant link, need to make a function and reuse code.
                    relevant_list = find_other_news_sources.find_other_news_sources(url=link)
                    if relevant_list is None or len(relevant_list) == 0:
                        if len(keypoints) > 100:
                            try:
                                # print keypoints
                                submission.add_comment(
                                    title + br + str(keypoints).encode('ascii', 'replace') + br + endmsg)
                                continue

                            except Exception as e:
                                print "3Unknown ERROR\n"
                                print type(e)
                                print e.args
                                print e
                                print submission.id
                                print "\n"
                                continue
                    else:
                        relevant_title = []
                        relevant_link = []
                        temp_alink = ""
                        temp_blink = ""
                        for a_link in relevant_list:
                            relevant_title.append(a_link[0])
                            relevant_link.append(a_link[1])

                        for (a_link, b_link) in itertools.izip(relevant_title, relevant_link):
                            if a_link is None:
                                a_link = "This"
                            if b_link is None or b_link == link:
                                continue
                            if temp_blink == b_link:
                                continue
                            try:
                                print "inside assertion"
                                relevant_message = relevant_message + "\n\n" + "> * " + "[" + a_link + "]" + "(" + b_link + ")"
                                temp_alink = a_link
                                temp_blink = b_link
                            except Exception as e:
                                print e


                                #relevant_message = relevant_message + "---"

                    if len(keypoints) > 150:
                        try:
                            # print keypoints
                            submission.add_comment(title + br + str(keypoints).encode('ascii',
                                                                                      'replace') + br + relevant_message + br + endmsg)

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
                #print "Id blocked or domain blocked"

                # if no more posts to summarize, go through unread messages and see if any posts to delete.
                unread = r.get_unread(limit=None)
                #print "here"
                for msg in unread:

                    # only works if the word delete is posted as it is, without edit.
                    if msg.body.lower() == 'delete':
                        try:

                            # get comment id from message.
                            #print "found one"
                            idd = msg.id
                            idd = 't1_' + idd
                            #print idd

                            # find comment from id
                            comment = r.get_info(thing_id=idd)

                            # find parent comment i.e samachar bot comment
                            parentid = comment.parent_id
                            #print parentid
                            comment_parent = r.get_info(thing_id=parentid)
                            sublink = comment_parent.link_id
                            author1 = r.get_info(thing_id=sublink)
                            #print author1.author
                            #print msg.author.name

                            # verify author of message is OP, then delete message and mark unread.
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
