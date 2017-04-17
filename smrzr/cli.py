import argparse
from core import summarize_url, summarize_text

def cli():
    parser = argparse.ArgumentParser(
            description="Get summary and key points from text")
    parser.add_argument('-f', '--file', \
            type=argparse.FileType('r'), help="filename containing text")
    parser.add_argument('-t', '--text', help="text string")
    parser.add_argument('-u', '--url', help="url string")
    parser.add_argument('-l', '--lines', type=int, help="number of sentences")
    args = vars(parser.parse_args())
    num_sentences = 4 if not args['lines'] else args['lines']

    if args['file']:
        try:
            text = args['file'].read()
            print "\n".join(summarize_text(text, \
                num_sentences=num_sentences))
        except Exception as e:
            print "error: ", e

    elif args['text']:
        print "\n".join(summarize_text(args['text'], \
                num_sentences=num_sentences))

    elif args['url']:
        res = summarize_url(args['url'],num_sentences=num_sentences)
        print "Summary: ", res[0]
        print "\nKey Points\n==========\n*", "\n* ".join(res[1])
