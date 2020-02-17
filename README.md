# Same-sex love songs 

Node scripts to gather the Billboard Hot 100 songs from each year between 2006–2019 for a project on explicit same-sex love interest songs.

## Setup

### Dependencies

- [node](https://nodejs.org/en/)
- [cheerio](https://cheerio.js.org/)
- [d3](https://d3js.org/)
- [request](https://www.npmjs.com/package/request)
- [fs](https://nodejs.org/api/fs.html)
- [lodash](https://lodash.com/)
- [python 3.X](https://www.anaconda.com/distribution/)

### Install

Clone the repo and run `npm i`

## Programmatic steps

#### `npm run get-billboard-html`

Pulls down html pages of the [Billboard Hot 100 songs](https://www.billboard.com/charts/year-end/2019/hot-100-songs) from each year between 2006–2019 and saves into the `output` folder as `billboard-{year}.html`

#### `npm run collect-songs`

Scrapes the html pages to collect the `year`, `rank`, `song`, and `artist` and saves into the `output` folder as `song-data.csv`

####`python ./process/s3_merge_lyrics.py {Personal Genius Client Access Token}`

Merges lyrics for Billboard songs listed in song-data.csv by pulling from local collection of .txt lyric files or using the Genius API. Adds cleaned lyrics to `lyrics` field and saves into the `output` folder as `song-data-lyrics.csv`.

Script uses the [LyricsGenius package](https://github.com/johnwmillr/LyricsGenius) (`pip install lyricsgenius`) to access the Genius API. A free account is required to obtain the *Client Access Token* referenced in the command line argument. After [signing up for an account](https://genius.com/signup_or_login), [create an API client](https://genius.com/developers) to recieve a personal *Client Access Token*. Additional API documentation is available [here](https://docs.genius.com/) if needed.

The Genius API was unable to find some lyrics using the original `song` and `artist` values in the data as search parameters. Alternate validated search parameters are provided in `genius-manual.csv` in the `process` folder and used in the script to successful merge all lyrics. 


#### `python ./process/s4_extract_features.py`

Parses lyrics to consider pronoun references. Adds `fempro` and `mascpro` pronoun indicator variables, `proref` category variable based on pronouns in lyrics and gender of artist, and `femphrases` and `mascphrases` variables documenting the context of pronoun references for further analysis

## Manual steps

### Artists' gender

Each artist was manually tagged as `male`, `female`, `mixed`, or `nb`. The `mixed` tag is used for musical groups or collaborations with a combination of male, female, or non-binary/genderfluid/genderqueer contributors. The `nb` tag is a simplified naming system to denote when the artist has explicited stated they identify as non-binary/genderfluid/genderqueer. Artists who released songs presenting as one gender and later indentifying differently were also tagged as `nb`. Genders were manually collected and verified using Google, Wikipedia, and artists' personal websites.
