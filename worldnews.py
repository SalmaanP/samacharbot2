import os
from goose import Goose
import praw
import MySQLdb
import urllib
import smrzr
from summary import summarize

active_subreddit = "worldnews"


class News(object):
    def assign(self, value, g, active_subreddit):

        url = value.url
        rid = value.id
        article = g.extract(url=url)
        text = article.cleaned_text
        meta = article.meta_description
        pdate = article.publish_date
        title = article.title

        try:
            imageurl = str(article.top_image.src)
            imagep = "D:\\newsaggsum\data\images" + "\\" + active_subreddit + "\\" + str(rid) + '.jpg'
            imagep = os.path.normpath(imagep)
        except AttributeError as a:
            print "Attribute Error"
            imageurl = None
            imagep = None
            pass

        return url, rid, article, text, meta, pdate, title, imageurl, imagep

    def __init__(self):
        pass


def main(active_subreddit):
    seen = 0
    analyzed = 0

    query = """INSERT INTO """ + active_subreddit + """ (id,link,domain,title,text,date,publish_date,image_path,summary,key_points,meta)
                               VALUES
                               (%s,%s,%s,%s,%s,CURDATE(),%s,%s,%s,%s,%s)"""

    newsobj = News()
    db = MySQLdb.connect(host="localhost",
                         user="test",
                         passwd="test123",
                         db="news",
                         charset="utf8",
                         use_unicode=True)
    cursor = db.cursor()
    g = Goose()
    r = praw.Reddit(user_agent='test')
    subreddit = r.get_subreddit(active_subreddit)
    submissions = subreddit.get_hot(limit=50)

    blocked = {"youtube.com", "imgur.com", "i.imgur.com", "imgflip.com", "flipkart.com",
               "snapdeal.com", "ebay.com", "blogs.wsj.com", "pbs.twimg.com", "twitter.com", "buzzfeed.com",
               "ptinews.com", "vine.co", "indigogo.com","en.wikipedia.com", "self." + active_subreddit, "niticentral.coms", "nytimes.com"}

    blockedid = {"37eomw"}
    for value in submissions:
        seen += 1

        print "Analysing new post " + value.domain
        if value.domain not in blocked and value.domain not in blockedid:

            try:
                (url, rid, article, text, meta, pdate, title, imageurl, imagep) = newsobj.assign(value, g,
                                                                                                 active_subreddit)
            except Exception as f:
                print "Unknown ERROR"
                print type(f)
                print f.args
                print f
                print value.id
                continue

            print rid+"\n"+url
            try:
                summ_article = smrzr.Summarizer(url)
                summary = summ_article.summary
                domain = value.domain
                if len(summary) > 500:
                    summary = summary[:500]+"..."
                keypoints = summ_article.keypoints
                # summary.encode('utf-8', 'ignore')
                keypoints = "<br><br>".join(keypoints)
                # keypoints.encode('utf-8', 'ignore')
                # print summary
                # print keypoints
                analyzed += 1
                urllib.urlretrieve(imageurl, "data/images/" + active_subreddit + "/" + rid + ".jpg")
                cursor.execute(query, (rid, url, domain, title, text, pdate, imagep, summary, keypoints, meta))
                print "Completed Analyzing\n"

            except smrzr.ArticleExtractionFail as b:
                print "Article Extraction Failed\n"
                continue

            except AssertionError as c:
                print "Assertion Error"
                summary = summarize(text, title)
                keypoints = summary
                domain = value.domain
                if len(summary) > 500:
                    summary = summary[:500]+"..."
                # summary.encode('utf-8', 'ignore')
                # keypoints = ''.join(keypoints)
                # keypoints.encode('utf-8', 'ignore')
                # print summary
                # print keypoints
                try:
                    cursor.execute(query, (rid, url, domain, title, text, pdate, imagep, summary, keypoints, meta))
                except Exception as e:
                    print type(e)
                    print e.args
                    continue
                analyzed += 1
                print "Assertion Error Handled"
                print "Completed Analyzing\n"
                continue

            except Exception as e:
                print "Unknown ERROR\n"
                print type(e)
                print e.args
                print e
                print value.id
                print "\n"
                continue

        else:

            print "Blocked URL...skipping\n"
            continue

    db.commit()
    cursor.close()
    db.close()
    print "Total Seen:"
    print seen
    print "Total Analyzed:"
    print analyzed


if __name__ == '__main__':
    main(active_subreddit)