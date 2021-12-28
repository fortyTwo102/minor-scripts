import urllib.request as urllib2
from bs4 import BeautifulSoup
import re
from pprint import pprint
import pickle
import json
import codecs
import time
import os


def fetch_ep_title(ep):


	ep2title_map = pickle.load(open('ep2title_map.pkl', 'rb'))

	return ep2title_map[int(ep)]

def scrape_text(url):

	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html, features="html.parser")

	####### FIRST METHOD - gets the raw text without any para breaks 

	# # kill all script and style elements
	# for script in soup(["script", "style"]):
	#     script.extract()    # rip it out

	# # get text
	# text = soup.get_text()
	# # print(text)
	# # break into lines and remove leading and trailing space on each
	# lines = (line.strip() for line in text.splitlines())
	# # break multi-headlines into a line each
	# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# # drop blank lines
	# page_text = '\n'.join(chunk for chunk in chunks if chunk)

	# # print(page_text)
	# # spoken_text_pattern = r'Written By\n([\s\S]*?)Previous\nPrevious\nEpisode\s'
	# spoken_text_pattern = r'Written By( Philosophize This!)?\n([\s\S]*?)Previous\nPrevious\nEpisode\s'
	# spoken_text = re.search(spoken_text_pattern, page_text).group(2)

	# return spoken_text

	####### SECOND METHOD - with the para breaks


	text_block = soup.find('div', attrs={'class': 'sqs-block-content'})

	# kill all script and style elements
	for script in text_block(["script", "style"]):
	    script.extract()    # rip it out

	paragraphs = text_block.findAll('p')
	paragraphs = [para.get_text() for para in paragraphs]
	spoken_text =  "\n".join(paragraphs)

	return spoken_text

def find_all_transcript_links(url):

	all_transcript_hrefs = list()
	ep2href_map = dict()
	exception_map = {

		'/transcript/2253': '139',
		'/transcript/transcript-government': '45',
		'/transcript/leibniz-pt-2-transcript': '38',
		'/transcript/leibniz-pt-1-transcript': '37',
		'/transcript/john-locke-pt-2-transcript': '36',
		'/transcript/john-locke-pt-1': '35',
		'/transcript/spinoza-pt-2-transcript': '34',
		'/transcript/spinoza-pt-1-transcript': '33',
		'/transcript/pascal-pt-2-transcript': '32',
		'/transcript/pascals-wager-transcript': '31',
		'/transcript/god-exists-transcript': '30',
		'/transcript/descartes-pt-2-transcript': '29',
		'/transcript/descartes-pt-1-transcript': '28',
		'/transcript/thomas-hobbes-transcript': '27',
		'/transcript/hobbes-pt-1-transcript': '26',
		'/transcript/saint-thomas-aquinas-philosophy': '21'
	}


	html_page = urllib2.urlopen(url)
	soup = BeautifulSoup(html_page)

	for link in soup.findAll('a', attrs={'href': re.compile("^/transcript/")}):

		all_transcript_hrefs.append(link.get('href'))

	for href in all_transcript_hrefs:

		try:
			regex_pattern = r'episode-(\d+)'
			episode_no = re.search(regex_pattern, href).group(1)

			ep2href_map[episode_no] = 'https://www.philosophizethis.org' + href
		except:
			print("Problem with", href)

	for href, ep in exception_map.items():
		ep2href_map[ep] = 'https://www.philosophizethis.org' + href

	ep2href_map = sorted(ep2href_map.items(), key=lambda x: int(x[0]))
	# pprint(ep2href_map)

	return ep2href_map

################ EXECUTION STARTS HERE ################

need_hrefmap = False

if need_hrefmap:
	ep2url_map = find_all_transcript_links('https://www.philosophizethis.org/transcripts')
	pickle.dump(ep2url_map, open("ep2href_map.pkl", "wb"))
else:
	ep2url_map = pickle.load(open("ep2href_map.pkl", "rb"))


final_transcripts = list()

for ep, url in ep2url_map:
	try:

		print("Downloading episode #", ep, end='')
		transcript = dict()
		spoken_text = scrape_text(url)

		transcript['ep'] = 'Episode #' + str(ep).zfill(3)
		transcript['title'] =  fetch_ep_title(ep)
		transcript['spoken_text'] = spoken_text

		final_transcripts.append(transcript)

		print("...Done")

		pickle.dump(final_transcripts, open("final_transcripts.pkl", "wb"))


		json_object = json.dumps(transcript, indent = 4)
		with codecs.open(os.path.join("transcript_utf_pb", "episode-" + ep + "-transcript.json"), 'w', encoding='utf-8') as f:
			json.dump(transcript, f, ensure_ascii=False)

		# with open(os.path.join("transcript_utf", "episode-" + ep + "-transcript.json"), "w", encoding="utf-8") as outfile:
		#     outfile.write(json_object)

		time.sleep(10)

	except Exception as e:

		print("\nProblem with ep #", ep, "with", url, e)
		time.sleep(10)



json_object = json.dumps(final_transcripts, indent=4)

with open("all_transcripts.json", "w", encoding="utf-8") as outfile:
    outfile.write(json_object)