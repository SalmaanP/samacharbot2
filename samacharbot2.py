# -*- coding: utf-8 -*-
__author__ = 'salmaan'

import praw
import smrzr
from altsummary import summary
import os
import find_other_news_sources
import itertools
from prawoauth2 import PrawOAuth2Mini
import blacklist
from time import sleep
import subreddits
from newspaper import Article
import message_templates as mt


def init():
    r = praw.Reddit(user_agent="Samachar Bot for /r/india by /u/sallurocks")
    scopes = {u'edit', u'submit', u'read', u'privatemessages', u'identity', u'history'}
    oauth_helper = PrawOAuth2Mini(r, app_key=os.environ['news_app_key'],
                                  app_secret=os.environ['news_app_secret'],
                                  access_token=os.environ['news_access_token'],
                                  refresh_token=os.environ['news_refresh_token'], scopes=scopes)
    subreddit = r.get_subreddit("+".join(subreddits.subreddits))
    return r, oauth_helper, subreddit


def postTracker():
    """File to keep track of posts already looked, gets refreshed if bot is restarted.
    put pointer at start, then reads the file to string and then puts the pointer back at the end."""

    fo = open("looked.txt", "a+")
    position = fo.tell()
    fo.seek(0, 0)
    str1 = fo.read()
    fo.seek(position)
    return fo, str1


def addSubmission(file_handler, submission):
    file_handler.write(submission.id + " ")


def isPosted(comments):
    for comment in comments:
        if str(comment.author) == 'samacharbot2':
            print "Already posted"
            return True
        else:
            return False


def summarizeSMRZR(url):
    """get post information and summary using Smrzr. Format properly."""

    summ_article = smrzr.Summarizer(url, 4, 'default', 'newspaper')
    keypoints = summ_article.keypoints
    summ = summ_article.summary
    message = "\n\n> * ".join(keypoints)
    message = "> * " + message
    message = message.replace("`", "")
    message = message.replace("#", "\#")
    return summ, message, summ_article.text


def processSummarization(file_handler, submission, method):
    if method == 'smrzr':
        addSubmission(file_handler, submission)

    if isPosted(submission.comments):
        print "already posted"
        return

    if method == 'smrzr':
        summ, keypoints, article_text = summarizeSMRZR(submission.url)
        print "Finished " + str(submission.id) + " with smrzr"
    elif method == 'other':
        summ, keypoints, article_text = summarizeOther(submission.url)
        print "Finished " + str(submission.id) + " with other"
    else:
        return

    if len(keypoints) < 150:
        return

    relevant_message = getRelevant(submission.url)

    if finalChecks(article_text):
        new_comment = summ + mt.br + keypoints.encode('ascii', 'ignore') + mt.br + relevant_message + mt.br + mt.endmsg
        postComment(submission, new_comment)


def summarizeOther(url):
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    keypoints = summary(text)
    summ = article.title
    keypoints = keypoints.replace("`", "")
    keypoints = keypoints.replace("#", "\#")

    return summ, keypoints, text


def finalChecks(text):
    if text == 'Never miss a great news story!\n\nGet instant notifications from Economic Times\n\nAllowNot ' \
               'now\n\nYou can switch off notifications anytime using browser settings.':
        print "check failed"
        return False
    else:
        return True


def postComment(submission, comment):
    try:
        submission.add_comment(comment)

    except Exception as e:
        print "Error posting comment\n"
        print type(e)
        print e.args
        print e
        print submission.id
        print "\n"


def getRelevant(link):
    relevant_list = find_other_news_sources.find_other_news_sources(url=link)
    if relevant_list is None or len(relevant_list) == 0:
        relevant_message = mt.relevant_message
    else:
        relevant_title = []
        relevant_link = []
        relevant_message = mt.relevant_message
        # temp variable to see if new link isn't same as last one.
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
                relevant_message = relevant_message + "\n\n" + "> * " + "[" + a_link + "]" + "(" + b_link + ")"
                temp_blink = b_link
            except Exception as e:
                print e

    return relevant_message


def checkDelete(r):
    unread = r.get_unread(limit=None)
    for msg in unread:

        # only works if the word delete is posted as it is, without edit.
        if msg.body.lower() == 'delete':
            try:

                # get comment id from message.
                idd = msg.id
                idd = 't1_' + idd

                # find comment from id
                comment = r.get_info(thing_id=idd)

                # find parent comment i.e samachar bot comment
                parentid = comment.parent_id
                comment_parent = r.get_info(thing_id=parentid)

                # get submission author through submission link id
                sublink = comment_parent.link_id
                author1 = r.get_info(thing_id=sublink)

                # verify author of message is OP, then delete message and mark unread.
                if str(msg.author.name) == str(author1.author):
                    comment_parent.delete()
                    msg.mark_as_read()
                else:
                    msg.mark_as_read()

            except Exception as e:
                print "Error in delete"
                print type(e)
                print e.args
                print e
                print "\n"
                msg.mark_as_read()
                continue


def checkConditions(submission, ids):
    return str(submission.domain) != str("self." + str(submission.subreddit)) \
           and submission.domain not in blacklist.blocked and submission.id not in ids


def start():

    r, oauth_helper, subreddit = init()

    while True:

        try:
            submissions = subreddit.get_new(limit=50)
        except praw.errors.HTTPException:
            print "HTTP Exception"
            sleep(300)
            continue

        nothing = True
        for submission in submissions:

            print "Working on - " + str(submission.id),
            fo, ids = postTracker()
            oauth_helper.refresh()

            if int(submission.score) >= 0:

                if checkConditions(submission, ids):
                    nothing = False
                    try:

                        processSummarization(fo, submission, 'smrzr')

                    except smrzr.ArticleExtractionFail:
                        print "Article Extraction Failed"
                        continue

                    # in case Smrzr fails to get summary, try another method
                    except AssertionError:
                        print "Assertion Error"
                        processSummarization(fo, submission, 'other')

                    except Exception as e:
                        print "Unknown ERROR"
                        print type(e)
                        print e.args
                        print e
                        print submission.id
                        print "\n"
                        continue

                    fo.close()

                else:
                    print "Nothing to do, checking messages"
                    # if no more posts to summarize, go through unread messages and see if any posts to delete.
                    checkDelete(r)
                    continue

        if nothing:
            print "Nothing to do, sleeping for 2 minutes"
            sleep(10)


if __name__ == '__main__':
    start()
