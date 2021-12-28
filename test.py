import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
from pprint import pprint
import pickle
import json


all_episodes_titles = list()
ep2title_map =  dict()
url = 'https://www.philosophizethis.org/podcasts'
title_regex = r'Episode\s[#\d]+([\s.…-]+)\s(.*)'
html_page = urllib2.urlopen(url)
soup = BeautifulSoup(html_page)

for link in soup.findAll('a'):

	all_episodes_titles.append(link.text)

all_episodes_titles = [x.strip() for x in all_episodes_titles if 'Episode' in x]

# pprint(all_episodes_titles)

for ep in range(1, 158):
	for title in all_episodes_titles:
		try:
			if str(ep) in " ".join(title.split(' ')[:2]):
				ep2title_map[ep] = re.search(title_regex, title).group(2)
		except:
			print("XXX, ", title)

pprint(ep2title_map)
pickle.dump(ep2title_map, open('ep2title_map.pkl', 'wb'))