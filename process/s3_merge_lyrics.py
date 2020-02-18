################################################################################
# Step 3: Merge Lyrics
#
# Script merges lyrics for Billboard songs listed in song-data.csv by either
# pulling from local collection of .txt lyric files or using the Genius API.
#
################################################################################

# Import packages
#---------------------------------------------
import pandas as pd
import os
import string
import re 
import lyricsgenius # pip install lyricsgenius
import argparse

# Setup
#---------------------------------------------

# Paths
csvpath = './output/song-data.csv'
lyricspath = './billboard_lyrics/lyrics/lyrics'
manualpath = './process/genius-manual.csv'
outputpath = './output/song-data-lyrics.csv'

# Read in songs data and list of lyrics files
data = pd.read_csv(csvpath)
lyricsfiles = [s for s in os.listdir(lyricspath)]

# Setup lyricsgenius access - Command line will need user's Genius "Access Token" (see documentation)
parser = argparse.ArgumentParser(description = 'Merge lyrics with Billboard songs')
parser.add_argument('geniustoken', nargs=1, type=str)
args = parser.parse_args()
accesstoken = args.geniustoken[0]
genius = lyricsgenius.Genius(accesstoken)

# Read in manual genius input changes and create lookup table
manual = pd.read_csv(manualpath)
manual['songartist'] = manual['song'] + "-" + manual['artist']
geniuslookup = manual[['songartist', 'geniussong', 'geniusartist']].set_index('songartist').to_dict('index')

# Add additional characters to remove from lyric text
string.punctuation = string.punctuation + "’…—”“,¡¿"

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

def getGeniusParameters(row):
	'''
	Takes a row of songs dataframe
	Checks if song is in the lookup table for manually verified Genius API parameters.
	(Future applications might want to replace *'s in song titles and take 1st artist of multiple artist entries to reduce manual lookups)
	If not in manual lookup table, the song and artist from the original data is sufficient (manually verified)
	'''
	# Create row key for lookup table
	songartist = row['song'] + "-" + row['artist']
	# Check if in manual lookup dictionary, get verified parameters if so
	if songartist in geniuslookup.keys():
		song = geniuslookup[songartist]['geniussong']
		artist = geniuslookup[songartist]['geniusartist']
	# If not in lookup table, original song and artist entries are sufficient parameters for Genius API (manually verified during testing)
	else:
		song = row['song']
		artist = row['artist']
	return song, artist

def cleanLyric(text):
	'''
	Takes string
	Cleans lyric text (removes line breaks, punctuation, lowercase, etc)
	'''
	# Remove Genius annotations, if in [] only - one song puts in () and does not get stripped (won't affect analysis)
	text = re.sub("[\[].*[\]]", " ", text)
	# Remove line breaks
	text = text.replace("\n", " ")
	# Remove punctuation
	text = text.translate(str.maketrans(dict.fromkeys(string.punctuation)))
	# Remove capitals
	text = text.lower()
	# Remove multiple spaces
	text = re.sub(" +", " ", text).strip()
	# Remove weird empty string thing
	text = text.replace("â€‹", "")
	return text

def getLyrics(row):
	'''
	Takes row of songs dataframe
	Pulls lyrics for each song in dataframe. Most songs are included in stored Billboard lyric files. 
	Lyrics are pulled using the Genius API (requires credentials) for those not included.
	'''
	# Get lyrics filename (for saved lyrics)
	lyricsfile = getLyricFilename(row)
	# Pull from saved billboard files if exists
	if lyricsfile in lyricsfiles:
		with open('./billboard_lyrics/lyrics/lyrics/{}'.format(lyricsfile), 'r') as file:
		    lyric = file.read()
		    lyric = cleanLyric(lyric)
	# Get lyrics using lyricsgenius API if not in saved files
	else:
		# Get parameters
		song, artist = getGeniusParameters(row)
		# Query Genius API
		geniussong = genius.search_song(song, artist)
		if geniussong != None:
			lyric = geniussong.lyrics
			lyric = cleanLyric(lyric)
		else:
			lyric = "ADD MANUALLY"
	return lyric

# Data process
#---------------------------------------------

# Remove duplicates (only keep first year the song appreared on the end of year charts)
data.drop_duplicates(subset = ['song', 'artist', 'gender'], keep = 'first', inplace = True) 

# Get Lyrics
data['lyrics'] = data.apply(getLyrics, axis=1)

# Write out
data.to_csv(outputpath, index=False, encoding='utf-8-sig')