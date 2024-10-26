from duckduckgo_search import DDGS
import praw

searcher = DDGS()

def search_reddit(product):
	query = product + " review site:reddit.com"
	results = [x['href'] for x in searcher.text(query) if "reddit" in x['href']]
	return results

print(search_reddit("Bissell Zing"))