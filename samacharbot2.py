__author__ = 'salmaan'

import sys
from goose import Goose
import praw
import smrzr
link="http://www.hindustantimes.com/bollywood/peepli-live-co-director-mahmood-faaroqui-arrested-on-rape-charges/article1-1361263.aspx"
summ_article = smrzr.Summarizer(link)
summary = summ_article.summary
print summary
sys.stdout.flush()