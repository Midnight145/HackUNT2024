import spacy
import eng_spacysentiment

nlp = eng_spacysentiment.load()

def get_tone(text):
    try:
        cats = nlp(text).cats
        pos = cats['positive']
        neg = cats['negative']
        neutral = cats['neutral']
        if pos > neg and pos > neutral:
            return pos
        elif neg > pos and neg > neutral:
            return -neg
        else:
            return 0
    except Exception as e:
        print("Error:", e)
        return 0