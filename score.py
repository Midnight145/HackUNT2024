from typing import Any

from tone import get_tone
from search import all_comments
import math

def get_scores(product) -> list[tuple[float | Any, Any]]:
	return [(get_tone(x[0].split(".")[0]) * math.sqrt(x[1]), x[0]) for x in all_comments(product) if x[1] > 0]


# noinspection PyTypeChecker
def parse(prod) -> dict:
	scores = get_scores(prod)
	avg = sum((x[0] for x in scores)) / len(scores)
	return {
		"num_reviews": len(scores),
		"average": sum((x[0] for x in scores)) / len(scores),
		"positive_reviews": len([x[0] for x in scores if x[0] > 0]),
		"negative_reviews": len([x[0] for x in scores if x[0] < 0]),
		"stars": round(2.5 * (avg + 1), 2),
		"highest": max(scores),
		"lowest": min(scores)
	}