import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

def summarize(string: str):
    doc = nlp(string)
    keyword = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    for token in doc:
        if token.text in STOP_WORDS or token.is_punct:
            continue
        if token.pos_ in pos_tag:
            keyword.append(token.text)
    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for word in freq_word.keys():
        freq_word[word] = (freq_word[word] / max_freq)

    sent_strength = {}
    for sent in doc.sents:
        for word in sent:
            if word.text in freq_word.keys():
                if sent in sent_strength.keys():
                    sent_strength[sent] += freq_word[word.text]
                else:
                    sent_strength[sent] = freq_word[word.text]

    summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
    final_sentences = [w.text for w in summarized_sentences]
    return ' '.join(final_sentences)

def get_tone(text):
    doc = nlp(summarize(text))
    return doc._.blob.polarity * (1 - doc._.blob.subjectivity)


print(get_tone(summarize("I love this product!! so super awesome!!")))


