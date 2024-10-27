from duckduckgo_search import DDGS
import praw
import json
from api import db

# noinspection PyTypeChecker
with open("client_info.json", "r") as f:
	info = json.loads(f.read())

reddit: praw.Reddit = praw.Reddit(
	client_id=info["client_id"],
	client_secret=info["client_secret"],
	user_agent="YOUR_USER_AGENT"
)
searcher = DDGS()

def search_reddit(product):
	query = product + " review site:reddit.com"
	results = [x['href'] for x, _ in zip(searcher.text(query), range(3)) if "reddit" in x['href']]
	return results

def get_comments(url):
	try:
		db_resp = db.fetch_review(url)
		if db_resp:
			vals = db_resp.get("values")
			print(f"Got {len(vals)} comments from the database")
			return [(val["body"], val["score"]) for val in vals]
		else:
			print("No comments found in the database, fetching from Reddit")
			submission = reddit.submission(url=url)
			submission.comments.replace_more(limit=0)
			db.push_item({
				"url": url,
				"values": [{"body": x.body, "score": x.score} for x in submission.comments if x.stickied == False]
			}, "reviews"),
			return [(x.body, x.score) for x in submission.comments if x.stickied == False]
	except Exception as e:
		print(f"An error occurred: {e}")
		return []

def all_comments(product):
	for x in search_reddit(product):
		for y in get_comments(x):
			yield y
