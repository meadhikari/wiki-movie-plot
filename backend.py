import os, sys; sys.path.insert(0, os.path.join("..", ".."))

from pattern.web import Wikipedia
import json
import urllib2
# This example retrieves an article from Wikipedia (http://en.wikipedia.org).
# A query requests the article's HTML source from the server, which can be quite slow.
# It is a good idea to cache results from Wikipedia locally,
# and to set a high timeout when calling Wikipedia.search().

engine = Wikipedia(language="en")

# Contrary to other search engines in the module,
# Wikipedia simply returns one WikipediaArticle object (or None) instead of a list of results.

def title_from_imdb(user_input):
	imdb_json_url = "http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q="+user_input.replace(" ","+")
	json_content = urllib2.urlopen(imdb_json_url)
	json_decoded = json.load(json_content)
	
	try: 
	    output = json_decoded["title_popular"][0]["title"]
	except:
		try:	
			output = json_decoded["title_approx"][0]["title"]
		except:
			try:
				output = json_decoded["title_approx"][0]["title"]
			except:
				output = user_input 
	
	return output	
	 
def plot(input):
    article = engine.search(input, cached=True, timeout=30)

    try:
        for s in article.sections:
            if s.title.upper() == "PLOT":
                return s.content
    except:
        return ""

