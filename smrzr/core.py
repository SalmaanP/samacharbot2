###################
# Author: Padmanabh
# License: Apache
###################

from better_sentences import better_sentences
from exceptions import ArticleExtractionFail
from formatters import Formatter
from goose import Goose
import networkx as nx
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_kernels
from utilities import memoize
from newspaper import Article

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
stemmer = nltk.stem.porter.PorterStemmer()


@better_sentences
def sentence_tokenizer(text):
    return sent_detector.tokenize(text)


@memoize
def goose_extractor(url):
    '''webpage extraction using
       Goose Library'''

    article = Goose().extract(url=url)
    return article.title, article.meta_description,\
                              article.cleaned_text


def newspaper_extractor(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
    except Exception as e:
        print e
        return None, None, None
    return article.title, article.meta_description, article.text


def _tokenize(sentence):
    '''Tokenizer and Stemmer'''

    _tokens = nltk.word_tokenize(sentence)
    tokens = [stemmer.stem(tk) for tk in _tokens]
    return tokens


def _normalize(sentences):
    '''returns tf-idf matrix
       (unigrams+bigrams)'''

    tfidf = TfidfVectorizer(tokenizer=_tokenize,
                            stop_words='english',
                            decode_error='ignore',
                            ngram_range=(1,2))
    return tfidf.fit_transform(sentences)


def _textrank(matrix):
    '''returns principal eigenvector
       of the adjacency matrix'''

    graph = nx.from_numpy_matrix(matrix)
    return nx.pagerank(graph)


def _intertext_score(full_text):
    '''returns tuple of scored sentences
       in order of appearance
       Note: Doing an A/B test to
       compare results, reverting to 
       original algorithm.'''

    sentences = sentence_tokenizer(full_text)
    norm = _normalize(sentences)
    similarity_matrix = pairwise_kernels(norm, metric='cosine')
    scores = _textrank(similarity_matrix)
    scored_sentences = []
    for i, s in enumerate(sentences):
        scored_sentences.append((scores[i],i,s))
    top_scorers = sorted(scored_sentences,
                         key=lambda tup: tup[0], 
                         reverse=True)
    return top_scorers


def _title_similarity_score(full_text, title):
    """Similarity scores for sentences with
       title in descending order"""

    sentences = sentence_tokenizer(full_text)
    norm = _normalize([title]+sentences)
    similarity_matrix = pairwise_kernels(norm, metric='cosine')
    return sorted(zip(
                     similarity_matrix[0,1:],
                     range(len(similarity_matrix)),
                     sentences
                     ),
                 key = lambda tup: tup[0],
                 reverse=True
                 )


def _remove_title_from_tuples(its, tss):
    index = None
    for i,el in enumerate(its):
        assert el[2] == tss[0][2], "fatal: tss and its don't align"
        index = i
    del its[index]
    del tss[0]
    return its, tss


def _aggregrate_scores(its,tss,num_sentences):
    """rerank the two vectors by
    min aggregrate rank, reorder"""
    final = []
    for i,el in enumerate(its):
        for j, le in enumerate(tss):
            if el[2] == le[2]:
                assert el[1] == le[1]
                final.append((el[1],i+j,el[2]))
    _final = sorted(final, key = lambda tup: tup[1])[:num_sentences]
    return sorted(_final, key = lambda tup: tup[0])


def _eval_meta_as_summary(meta):
    """some crude heuristics for now
    most are implemented on bot-side
    with domain whitelists"""

    if meta == '':
        return False
    if len(meta)>500:
        return False
    if 'login' in meta.lower():
        return False
    return True


def summarize_url(url, num_sentences=4, fmt='default'):
    '''returns: tuple containing
       * single-line summary candidate 
       * key points
       in the format specified.
    '''

    #title, meta, full_text = goose_extractor(url)
    title, meta, full_text = newspaper_extractor(url)

    if not full_text:
        raise ArticleExtractionFail("Couldn't extract: {}".format(url))

    its = _intertext_score(full_text)
    tss = _title_similarity_score(full_text,title)

    if _eval_meta_as_summary(meta):
        summ = meta
        if tss[0][2].lower() in summ.lower():
            its, tss = _remove_title_from_tuples(its, tss)
        elif summ.lower() in tss[0][2].lower():
            summ = tss[0][2]
            its, tss = _remove_title_from_tuples(its, tss)
    else:
        summ = tss[0][2]
        its, tss = _remove_title_from_tuples(its, tss)

    scores = [score[2] for score in _aggregrate_scores(its, tss, num_sentences)]
    formatted = Formatter(scores, fmt).frmt()
    return summ, formatted


def summarize_text(full_text, num_sentences=4, fmt='default'):
    its = _intertext_score(full_text)[:num_sentences]
    kpts = [k[2] for k in sorted(its, key = lambda tup: tup[1])]
    return kpts
