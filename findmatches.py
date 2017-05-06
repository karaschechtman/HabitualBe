import re

PRONOUNS = ['i','you','he','she','we','they']
AUX = ['unless','demanding','ef','how','wherever','may','though','providing','dare','whether','that','can','t ','shall','suppose','should','till','since','as','would','could','will','lest','if']


'''
Reads in some text to find any constructions of preceding word + pronoun + be + word
:param filename: the name of the file to check for auxiliaries
:param ing: set to True if you want to get only habitual be candidates
:returns: array of strings of habitual be candidates
'''
def find_be_candidates(filename,ing=True):
	with open(filename,"r") as myfile:
		data = myfile.read().replace('\n','').lower()

	prons = '|'.join(PRONOUNS)

	if ing:
		return re.findall('(?:' + prons + ') be [a-z]*ing',data)
	else:
		return re.findall('(?:[a-z]* )(?:' + prons + ') be [a-z]*',data)

'''
Filters against common disqualifying auxiliaries
:param possibilities: array of possible habitual be candidates
:returns: array of habitual be candidates that do not contain auxiliaries
'''
def check_auxiliaries(possibilities):
	realities = []
	for possibility in possibilities:
		if not any(auxil in possibility for auxil in AUX):
 			realities.append(possibility)
	return realities

'''
Checks a file to find habitual be candidates
:filename: the name of the file to check
'''
def check_file(filename):
	possibilities = find_be_candidates(filename,False)
	realities = check_auxiliaries(possibilities)
	return realities

'''
Run be test on all files in a dir and save results to spreadsheet
'''
def main(dir):
	for file in os.listdir(dir):
		results = check_file(path.join(dir,file))
		if len(results) > 0:
			i +=1
			print file + ':'
			print results
	print 'Total results: ' + str(i)

main('gutenberg')
