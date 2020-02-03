# Import packages
#---------------------------------------------
import pandas as pd
import os
import string

# Read in data
#---------------------------------------------

# Paths
csvpath = './output/song-data.csv'
lyricspath = './billboard_lyrics/lyrics/lyrics'

# Read in songs data and list of lyrics files
data = pd.read_csv(csvpath)
lyricsfiles = [s for s in os.listdir(lyricspath)]


# Functions
#---------------------------------------------

def getLyricFilename(row):
	'''
	Takes row of songs dataframe
	Constructs filename string in the format needed for saved Billboard song lyric .txt files
	'''
	# Get artist part of file (replace spaces with _ and take 1st 15 characters)
	artist_search = row['artist'].replace(" ", "_")[:15]
	# Get song part of file (replace spaces with _ and take 1st 20 characters)
	song_search = row['song'].replace(" ", "_")[:20]
	# Construct file name
	lyricsfile = artist_search + '-' + song_search + ".txt"
	return lyricsfile

def cleanLyric(text):
	'''
	Takes string
	Cleans lyric text (removes punctuation, lowercase)
	'''
	# Remove punctuation
	text = text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
	# Remove capitals
	text = text.lower()
	return text

def getLyrics(row):
	'''
	Takes row of songs dataframe
	Pulls lyrics for each song in dataframe. Most songs are included in stored Billboard lyric files. Lyrics are scraped (TODO) for those not included.
	'''
	# Get lyrics filename (for saved lyrics)
	lyricsfile = getLyricFilename(row)
	# Pull from saved billboard files if exists
	if lyricsfile in lyricsfiles:
		with open('./billboard_lyrics/lyrics/lyrics/{}'.format(lyricsfile), 'r') as file:
		    lyric = file.read().replace('\n', '')
		    lyric = cleanLyric(lyric)
	# Scrape lyrics if not in saved files
	else:
		lyric = "not in saved files"
	return(lyric)

# Data process
#---------------------------------------------

# Remove duplicates (only keep first year the song appreared on the end of year charts)
data.drop_duplicates(subset = ['song', 'artist', 'gender'], keep = 'first', inplace = True) 

# Get Lyrics
data['lyrics'] = data.apply(getLyrics, axis=1)

print(data.head(20))