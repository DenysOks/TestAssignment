from bs4 import BeautifulSoup
import requests
import re


def get_amazon_com_html(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3)'}
	page = requests.get(url, headers=headers)
	html_soup = BeautifulSoup(page.content, 'html.parser')
	return html_soup


def extract_text_from_html(url):
	list_of_urls = list()
	soup = get_amazon_com_html(url)
	# remove all javascript and stylesheet code
	for script in soup(["script", "style"]):
		script.decompose()
	# get list of links
	for a in soup.find_all('a', href=True):
		if "amazon.com" in a['href']:
			list_of_urls.append(a['href'])

	# extract text and get rid of all href
	all_text = soup.get_text()
	for link in soup.find_all('a'):
		if 'href' in link.attrs:
			text = link.get_text()
			link.clear()
			link.append(text)
	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in all_text.splitlines())
	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	# remove empty lines
	all_text = '\n'.join(chunk for chunk in chunks if chunk)
	word_set = set()
	text = [re.sub(r"[^a-zA-Z']+", ' ', k) for k in all_text.split("\n")]
	for string in text:
		word_set.update(string.split())
	return word_set, list_of_urls


def find_sentence_on_amazon(sentence="Virtue signalling is society's version of Proof of Stake",
							url="https://www.amazon.com/"):
	desired_words = sentence.split()
	words_left_to_find = desired_words.copy()
	word_dictionary, list_of_urls = extract_text_from_html(url)
	for current_word in desired_words:
		for word in word_dictionary:
			if current_word.lower() == word.lower():
				words_left_to_find.remove(current_word)
				break
	if len(words_left_to_find) > 0:
		print("Cannot to recreate the following sentence: %s \nUsing url: %s " % (sentence, url))
		# find_sentence_on_amazon(sentence=" ".join(words_left_to_find), url=list_of_urls.pop())
		# TODO! Need more time to implement search in all amazon
	else:
		print("Sentence: %s. Has been successfully recreated using url: %s " % (sentence, url))


if __name__ == "__main__":
	find_sentence_on_amazon()
