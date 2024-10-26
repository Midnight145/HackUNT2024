import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')
text = """
I bought a bagged Zing about six months ago, and to be honest I'm not sure I'd recommend it in your case.

I'll start off by saying that it does a good job on hard floors, and it's hard to beat the price.

But I just don't like using it. The large rear wheels and somewhat rigid hose mean you have to be purposeful about how you move to prevent it from getting stuck or flipping over. The wand is also too short for my 6' stature, and the floor tool vertical pivot is limited in a way that make it awkward to maneuver in tight spaces or get under large furniture. Granted, you can replace the floor tool and wand, but upgrading those would cost at least as much as the vacuum itself.

In retrospect, I wish I'd bit the bullet and upped my budget for a Miele C1 or Kenmore 200 series. I'd definitely second u/performancereviews recommendation to go to a vacuum store and try out a canister. That will give you a better idea of whether you like canisters anyways, since the weak points of the Zing belie the reasons that some people prefer canister vacs.
"""
doc = nlp(text)


print(doc._.blob.polarity)