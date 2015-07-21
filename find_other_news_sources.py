# __author__ = 'sree'
import urllib2
from lxml import html
import requests
from goose import Goose

g = Goose()


def get_page_tree(url=None):
    page = requests.get(url=url, verify=False)
    return html.fromstring(page.text)


def get_title(url=None):
    try:
        article = g.extract(url=link)
        return article.title
    except Exception as e:
        try:
            tree = get_page_tree(url=url)
            return tree.xpath('//title//text()')[0].strip().split(' -')[0]
        except Exception as b:
            return None


def find_other_news_sources(url=None, title=None):
    # Google forwards the url using <google_domain>/url?q=<actual_link>. This might change over time
    forwarding_identifier = '/url?q='
    if not title:
        try:
            title = get_title(url=url)
        except Exception as e:
            return None
    try:
        # parent_url_exclude = '-site:' + url
        #google_news_search_url = 'http://www.google.com/search?q=' + urllib2.quote(title) + parent_url_exclude + '&tbm=nws'
        google_news_search_url = 'http://www.google.com/search?q=' + urllib2.quote(title) + '&tbm=nws'
        google_news_search_tree = get_page_tree(url=google_news_search_url)
        other_news_sources_links = [a_link.replace(forwarding_identifier, '').split('&')[0] for a_link in
                                    google_news_search_tree.xpath('//a//@href') if forwarding_identifier in a_link]
    except Exception as e:
        return None

    new_links = []
    count = 0
    for a_link in other_news_sources_links:
        try:
            article = g.extract(a_link)
            title = article.title
            templist = [title, a_link]
            new_links.append(templist)
            count = count + 1
            print count
        except Exception as e:
            print "1Unknown ERROR\n"
            print type(e)
            print e.args
            print e
            # print submission.id
            print "\n"
            continue

        if count is 4:
            break

    return new_links
