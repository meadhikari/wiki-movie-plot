import json
import urllib2
def title_from_imdb(user_input="Inception"):
	
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
	
	
	
print title_from_imdb()	
