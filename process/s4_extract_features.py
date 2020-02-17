# Import packages
#---------------------------------------------
import pandas as pd

# Read in data
#---------------------------------------------
lyricdatapath = './output/song-data-lyrics.csv'
data = pd.read_csv(lyricdatapath)

# Flag pronouns used
#---------------------------------------------

# Pad spaces (instead of tokenizing?)
data['lyrics'] = " " + data['lyrics'] + " "

# List of pronouns to search for
fempronouns = [' she ', ' shes ', ' shed ', ' her ', ' hers ', ' herself '] 
mascpronouns = [' he ', ' hes ', ' hed ', ' him ', ' his ', ' himself ']

# Flag which pronouns used
data['fempro'] = data['lyrics'].apply(lambda x: any([p in x for p in fempronouns])).astype(int)
data['mascpro'] = data['lyrics'].apply(lambda x: any([p in x for p in mascpronouns])).astype(int)


# Flags related to artist identity
#---------------------------------------------

# Categorize songs
def referenceType(data):
	'''
	Catagorizes songs based on the gender of the artist and pronouns referenced in the lyrics
	'''
	if data['fempro'] == 0 & data['mascpro'] == 0:
		return 'No reference'
	elif data['fempro'] == 1 & data['mascpro'] == 1:
		return 'Masc & fem reference'
	elif (data['gender'] == 'man' and data['mascpro'] == 1) | (data['gender'] == 'woman' and data['fempro'] == 1):
		return 'Same-gender'
	elif (data['gender'] == 'man' and data['fempro'] == 1) | (data['gender'] == 'woman' and data['mascpro'] == 1):
		return 'Opposite-gender'


data['proref'] = data.apply(referenceType, axis=1)

# Quick table
print(data['proref'].value_counts())

# Grab pronoun phrases (for easier characterizing?)
#---------------------------------------------

# TODO - if taking too long, only do this for ones that contain the pronoun

# Create regex's
def proPhraseRegex(pronounlist):
	'''
	Takes a List
	Creates a regex to match the phrase (5 words before and after) a pronoun search term
	Wont get phrases at the beginning or end of song, regex to capture those too took too long
	'''
	regex = '(?:[a-z]+ ){5}[a-z]+'
	for p in pronounlist[:-1]:
		regex = regex + p + '(?:[a-z]+ ){5}[a-z]+' + '|' + '(?:[a-z]+ ){5}[a-z]+'
	return regex + pronounlist[-1] + '(?:[a-z]+ ){5}[a-z]+'

# Extract pronoun phrases, remove dups (maybe should keep?)
data['femphrases'] = data['lyrics'].str.findall(proPhraseRegex(fempronouns))
data['femphrases'] = [', '.join(map(str, l)) for l in list(map(set,data['femphrases']))]
data['mascphrases'] = data['lyrics'].str.findall(proPhraseRegex(mascpronouns))
data['mascphrases'] = [', '.join(map(str, l)) for l in list(map(set,data['mascphrases']))]

#print(data)

# Write out
#---------------------------------------------
outputpath = './output/song-data-plus.csv'
data.to_csv(outputpath, index=False)