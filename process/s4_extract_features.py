# Import packages
#---------------------------------------------
import pandas as pd

# Read in data
#---------------------------------------------
inputpath = '../output/song-data.csv'
data = pd.read_csv(inputpath)


#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------

# TEMP - Insert test lyrics
#---------------------------------------------

testlyric = 'Uh Yeah yeah When I was young I fell in love We used to hold hands man that was enough (yeah) Then we grew up started to touch Used to kiss underneath the light on the back of the bus (yeah) Oh no your daddy didnt like me much And he didnt believe me when I said you were the one Oh every day she found a way out of the window to sneak out late She used to meet me on the Eastside In the city where the sun dont set And every day you know that we ride Through the backstreets of a blue Corvette Baby you know I just wanna leave tonight We can go anywhere we want Drive down to the coast jump in the seat Just take my hand and come with me yeah We can do anything if we put our minds to it Take your whole life then you put a line through it My love is yours if youre willing to take it Give me your heart cause I aint gonna break it So come away starting today Start a new life together in a different place We know that love is how these ideas came to be So baby run away away with me Seventeen and we got a dream to have a family A house and everything in between And then oh suddenly we turned twenty-three Now we got pressure for taking our life more seriously We got our dead-end jobs and got bills to pay Have old friends and know our enemies Now I Im thinking back to when I was young Back to the day when I was falling in love He used to meet me on the Eastside In the city where the sun dont set And every day you know where we ride Through the backstreets in a blue Corvette And baby you know I just wanna leave tonight We can go anywhere we want Drive down to the coast jump in the seat Just take my hand and come with me Singing We can do anything if we put our minds to it Take your whole life then you put a line through it My love is yours if youre willing to take it Give me your heart cause I aint gonna break it So come away starting today Start a new life together in a different place We know that love is how these ideas came to be So baby run away with me Run away now Run away now Run away now Run away now Run away now Run away now He used to meet me on the Eastside She used to meet me on the Eastside He used to meet me on the Eastside She used to meet me on the Eastside In the city where the sun dont set'
#'This was never the way I planned Not my intention I got so brave drink in hand Lost my discretion Its not what Im used to Just wanna try you on Im curious for you Caught my attention I kissed a girl and I liked it The taste of her cherry chap stick I kissed a girl just to try it I hope my boyfriend dont mind it It felt so wrong It felt so right Dont mean Im in love tonight I kissed a girl and I liked it I liked it No I dont even know your name It doesnt matter Youre my experimental game Just human nature Its not what good girls do Not how they should behave My head gets so confused Hard to obey I kissed a girl and I liked it The taste of her cherry chap stick I kissed a girl just to try it I hope my boyfriend dont mind it It felt so wrong It felt so right Dont mean Im in love tonight I kissed a girl and I liked it I liked it Us girls we are so magical Soft skin red lips so kissable Hard to resist so touchable Too good to deny it Aint no big deal its innocent I kissed a girl and I liked it The taste of her cherry chap stick I kissed a girl just to try it I hope my boyfriend dont mind it It felt so wrong It felt so right Dont mean Im in love tonight I kissed a girl and I liked it I liked it'


data['lyrics'] = testlyric
data['lyrics'] = data['lyrics'].str.lower() # Clean in step 3? - strip punctuation, lowercase

#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------


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
	elif (data['gender'] == 'male' & data['mascpro'] == 1) | (data['gender'] == 'female' & data['fempro'] == 1):
		return 'Same-sex'
	elif (data['gender'] == 'male' & data['fempro'] == 1) | (data['gender'] == 'female' & data['mascpro'] == 1):
		return 'Opposite-sex'


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
	Wont get phrases at the beginning or end of song, regex to capture those too took too long (commented out)
	'''
	regex = '(?:[a-z]+ ){5}[a-z]+'
	for p in pronounlist[:-1]:
		regex = regex + p + '(?:[a-z]+ ){5}[a-z]+' + '|' + '(?:[a-z]+ ){5}[a-z]+'
	return regex + pronounlist[-1] + '(?:[a-z]+ ){5}[a-z]+'
	
	# regex = '(?:[a-z]* *){5}[a-z]*'
	# for p in pronounlist[:-1]:
	# 	regex = regex + p + '(?:[a-z]* *){5}[a-z]*' + '|' + '(?:[a-z]* *){5}[a-z]*'
	# return regex + pronounlist[-1] + '(?:[a-z]* *){5}[a-z]*'

# Extract pronoun phrases, remove dups (maybe should keep?)
data['femphrases'] = data['lyrics'].str.findall(proPhraseRegex(fempronouns))
data['femphrases'] = [','.join(map(str, l)) for l in list(map(set,data['femphrases']))]
data['mascphrases'] = data['lyrics'].str.findall(proPhraseRegex(mascpronouns))
data['mascphrases'] = [','.join(map(str, l)) for l in list(map(set,data['mascphrases']))]

#print(data)

# Write out
#---------------------------------------------
outputpath = '../output/song-data-plus.csv'
data.to_csv(outputpath, index=False)