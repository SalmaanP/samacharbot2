# __author__ = 'sree'
import find_other_news_sources

def run_example():
    print 'running'
    links = find_other_news_sources.find_other_news_sources(
        url='http://timesofindia.indiatimes.com/tech/tech-news/Local-WhatsApp-Viber-Skype-calls-may-no-longer-be-free/articleshow/48106038.cms')
    for a_link in links:
        print a_link
run_example()