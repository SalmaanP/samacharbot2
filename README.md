# samacharbot2

Reddit bot which summarizes link containing news articles on /r/india subreddit.

Uses two summarizing libraries

1)[Smrzr](https://github.com/lekhakpadmanabh/Summarizer)

2)[Sumy](https://github.com/miso-belica/sumy)

Uses [Newspaper](https://github.com/codelucas/newspaper/) for scraping content.

Thanks to [sr33](https://github.com/sr33/OtherNewsSources) for relevant news links idea and implementation

Find the bot on reddit [here](https://www.reddit.com/u/samacharbot2)

# Code

The main files are [samacharbot2.py](https://github.com/HunkDivine/samacharbot2/blob/master/samacharbot2.py), [altsummary.py](https://github.com/HunkDivine/samacharbot2/blob/master/altsummary.py) and [blacklist.py](https://github.com/HunkDivine/samacharbot2/blob/master/blacklist.py), ignore the rest, they are either config files for heroku or files for testing.

# Contribute

Help me in identifying websites which break the bot which provide summaries like "Javascript is not enabled" or "Email not sent" or other such messages.

Fork, edit the [blacklist file](https://github.com/HunkDivine/samacharbot2/blob/master/blacklist.py) by appending domain name (you can check this by reading what's written next to the reddit title in brackets) to it and send a pull request!

Thanks!


# Subreddits

Currently working on the following subreddits:

* india
* TESTBOTTEST
* TILinIndia
* willis7737_news
* freesoftware
* parabola
* libreboot
* mumbai
* UpliftingKhabre
