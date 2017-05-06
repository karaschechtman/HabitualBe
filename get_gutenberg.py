import numpy as np
import pandas as pd
import urllib
import os
from os import path
import zipfile
import shutil

'''Loads metadata to memory from the Gutenberg HDF and determines which are American fiction
:return: metadata on works of American Fiction in Gutenberg
'''
def load_american_gutenberg():
	df = pd.read_hdf('pg-metadata-rdf.hdf','pg-metadata')
	df = df.T
	df['AmericanFiction'] = df['LCC'].apply(_checkAmerSubject_)
	american = df.loc[(df['AmericanFiction'] == True)]
	return american



'''Download text/HTML files from Gutenberg for works of American Fiction
'''
def download_files(american):
	to_download = []
	for file_candidate in american['formats']:
		if 'text/html' in file_candidate.keys():
			to_download.append(file_candidate['text/html'])

	for filename in to_download:
		urllib.urlretrieve(filename,path.join('gutenberg',filename.rsplit('/',1)[-1]))

'''
Unzip all files in directory gutenberg/
'''
def unzip_files():
	zips = [file for file in os.listdir('gutenberg') if file.endswith('.zip')]
	for zip in zips:
		zip_ref = zipfile.ZipFile(path.join('gutenberg',zip),'r')
		zip_ref.extractall('gutenberg')
		zip_ref.close()


'''
Cleans data in Gutenberg once downloaded
'''
def clean_data():
	for thing in os.listdir('gutenberg'):
		if path.isdir(path.join('gutenberg',thing)):
			for myfile in os.listdir(path.join('gutenberg',thing)):
				if not path.isdir(path.join('gutenberg',thing,myfile)):
					shutil.copy(path.join('gutenberg',thing,myfile),path.join('gutenberg',myfile))
			shutil.rmtree(path.join('gutenberg',thing))
		if thing.endswith('.jpg') or thing.endswith('.png') or thing.endswith('.zip'):
			os.remove(path.join('gutenberg',thing))


"""
Checks if the subject from a list of LOC subjects is AmericanFiction
:param subjects: list of subjects
:return: True if American, False otherwise
"""
def _checkAmerSubject_(subjects):
	return True if 'PS' in subjects else False

'''
Download and prepare all files named Gutenberg
There must be a directory gutenberg/ to save in
'''
def main():
    american = load_american_gutenberg()
	download_files(american)
	unzip_files()
	clean_data()
