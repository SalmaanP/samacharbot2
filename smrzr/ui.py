"""
just providing a convenient UI
"""
from core import summarize_url

class Summarizer:

    def __init__(self, url, num_sentences=4, 
                 fmt='default', extractor=None):

        self.url = url

        if not extractor:
            from core import goose_extractor 
            self._extr = goose_extractor
        else:
            from core import newspaper_extractor
            self._extr = newspaper_extractor

        self.title, self.meta, self.text = self._extr(url)

        self.summary, self.keypoints = \
            summarize_url(self.url, num_sentences, fmt)

    def __str__(self):
        return "Summarizer object for {}".format(self.url)
