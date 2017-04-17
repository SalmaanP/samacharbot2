from functools import wraps

def better_sentences(func):
    """takes care of some edge cases of sentence
    tokenization for cases when websites don't
    close sentences properly, usually after
    blockquotes, image captions or attributions"""

    @wraps(func)
    def wrapped(*args):

            sentences = func(*args)
            new_sentences = []
            for i, l in enumerate(sentences):
                if '\n\n' in l:
                    splits = l.split('\n\n')
                    if len(splits)>1:
                        for ind,spl in enumerate(splits):
                            if len(spl) <20:
                                #if DEBUG: print "Discarding: ", spl
                                del splits[ind]
                    new_sentences.extend(splits)
                else:
                    new_sentences.append(l)
            return new_sentences
    return wrapped

