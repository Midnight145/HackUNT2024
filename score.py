from tone import get_tone
from search import all_comments
import math

def get_scores(product):
	return [get_tone(x[0].split(".")[0]) * math.sqrt(x[1]) for x in all_comments(product) if x[1] > 0]

scores = get_scores("Expedia")

avg = sum(scores) / len(scores)

print("Num Reviews: ", len(scores))
print("Average: ", avg)
print("Positive reviews: ", len([x for x in scores if x > 0]))
print("Negative reviews: ", len([x for x in scores if x < 0]))
print("Stars: ", round(2.5 * (avg + 1), 2))