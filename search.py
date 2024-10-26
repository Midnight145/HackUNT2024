from duckduckgo_search import DDGS
import praw
import json


searcher = DDGS()

with open("client_info.json", "r") as f:
	info = json.loads(f.read())

reddit = praw.Reddit(
	client_id = info["client_id"],
	client_secret = info["client_secret"],
	user_agent = "YOUR_USER_AGENT"
)

def search_reddit(product):
	query = product + " review site:reddit.com"
	results = [x['href'] for x in searcher.text(query) if "reddit" in x['href']]
	return results

#print(search_reddit("Bissell Zing"))


def get_comments_from_posts(urls):
	comments_data = []

	for url in urls:
		try: 
			submission = reddit.submission(url=url)
			submission.comments.replace_more(limit=0)

			for comment in submission.comments.list():
				comments_data.append({
					"comment": comment.body,
					"upvotes": comment.score
				})
		except Exception as e:
			print(f"An error occurred: {e}")
	return comments_data

product_urls = search_reddit("Bissell Zing")
comments_and_upvotes = get_comments_from_posts(product_urls)
for item in comments_and_upvotes:
	print("comment:", item["comment"])
	print("Upvotes:", item["upvotes"])
	print("-" * 50)