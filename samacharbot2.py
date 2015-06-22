__author__ = 'salmaan'

import sys
from goose import Goose
import praw
import smrzr
reload(sys)
sys.setdefaultencoding('UTF8')
link="http://www.newindianexpress.com/nation/Man-Caught-Urinating-in-Delhi-Metro-Disturbed-Passenger-Uploads-Video-in-Social-Media/2015/06/21/article2878562.ece"
summ_article = smrzr.Summarizer(link)
summaryy = summ_article.summary
print summaryy.encode("utf=8")
