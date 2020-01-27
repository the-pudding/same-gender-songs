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

### Install

Clone the repo and run `npm i`

## Programmatic steps

#### `npm run get-billboard-html`

Pulls down html pages of the [Billboard Hot 100 songs](https://www.billboard.com/charts/year-end/2019/hot-100-songs) from each year between 2006–2019 and saves into the `output` folder as `billboard-{year}.html`

#### `npm run collect-songs`

Scrapes the html pages to collect the `year`, `rank`, `song`, and `artist` and saves into the `output` folder as `song-data.csv`

## Manual steps

### Artists' gender

Each artist was manually tagged as `male`, `female`, `mixed`, or `nb`. The `mixed` tag is used for musical groups or collaborations with a combination of male, female, or non-binary/genderfluid/genderqueer contributors. The `nb` tag is a simplified naming system to denote when the artist has explicited stated they identify as non-binary/genderfluid/genderqueer. Artists who released songs presenting as one gender and later indentifying differently were also tagged as `nb`. Genders were manually collected and verified using Google, Wikipedia, and artists' personal websites.