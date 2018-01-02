import re
import csv
import os
from nltk.tokenize import RegexpTokenizer
from os import path
from bs4 import BeautifulSoup

AM = 'am'
AND = 'and'
ENCODING = 'utf-8'
I_PRON = 'i'
IVE = 'ive'
MA = 'ma' # because of ma'am
MATCH_FOUND_MSG = 'MATCH FOUND: '
PARSER = 'html.parser'
WHO = 'who'

FORBIDDEN_WORDS = [AND, I_PRON, IVE, MA, WHO]
'''
Gets all words from a file's HTML, stripped of punctuation, in a list
:param filename: the name of the file to get words from
'''
def get_words(filename):
	with open(filename,"r") as myfile:
		data = myfile.read().replace('\n',' ').replace("'",'').lower()
		soup = BeautifulSoup(data, PARSER)
		text = soup.getText()
		tokenizer = RegexpTokenizer(r'\w+')
		words = tokenizer.tokenize(text)
		return words
'''
Looks in a list of words to find any constructions of preceding word + pronoun
+ am + following word where preceding and following words within a certain
interval are not the pronoun "I" or other words likely to signal its presence.
:param words: the list of words
:param interval: the interval of surroundings words in which to search for "I"
:returns: array of strings of habitual be candidates
'''
def find_am_candidates(words, interval):
	results = []
	for i in range(0, len(words)):
		word = words[i]
		if word == AM:
			prev_words = words[i-interval:i]
			next_words = words[i+1:i+interval+1]
			surrounding_words = prev_words + next_words
			if not any(word in surrounding_words for word in FORBIDDEN_WORDS):
				am_phrase = ' '.join(word for word in prev_words) + ' ' + (
					word + ' ' + ' '.join(word for word in next_words))
				print MATCH_FOUND_MSG + am_phrase
				results.append(am_phrase)
	return results

'''
Checks a directory of test files for am canditates.
:param dir: the directory to check
:param csvname: the csvname in which to store results
:param interval: the interval in which to search for "I" (see find_am_candidates)
'''
def check_directory(dir,csvname, interval):
	with open(csvname,'wb') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['Title','Year','Comments','Filename'])
		for file in os.listdir(dir):
			words = [word.encode(ENCODING) for word in get_words(path.join(dir,file))]
			results = find_am_candidates(words, interval)
			if len(results) > 0:
				writer.writerow(['','','',file] + results)
		csvfile.close()

'''
Run be test on all files in a dir and save results to spreadsheet
'''
def main():
	dir = raw_input('What directory do you want to run the script on? ')
	interval = raw_input('In what interval do you want to search pron I? ')
	check_directory(dir, dir + '.csv', int(interval))

main()
