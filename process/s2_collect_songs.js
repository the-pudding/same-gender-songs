const fs = require('fs');
const d3 = require('d3');
const request = require('request');
const cheerio = require('cheerio');

const IN_PATH = './output'
const OUT_PATH = './output'
const YEARS = d3.range(2006, 2021)
const songData = [];

function getSongs(year) {
    console.log(year)

    const FILE = fs.readFileSync(`${IN_PATH}/billboard-${year}.html`, `utf-8`)
    const $ = cheerio.load(FILE)

    $('.chart-details__item-list')
        .each((i, el) => {
            const ARTICLE = $(el).find('article')
            ARTICLE.each((i, el) => {
               const ROW = $(el).find('.ye-chart-item__primary-row ')
               const rank = ROW.find('.ye-chart-item__rank').text().trim()
               const TEXT = ROW.find('.ye-chart-item__text')
               const song = TEXT.find('.ye-chart-item__title').text().trim()
               const artist = TEXT.find('.ye-chart-item__artist').text().trim()

               if (artist != undefined) songData.push({year, rank, song, artist})   
            })
        })
        return songData
}

function init() {
    YEARS.map(getSongs);

    const concatSongData = [].concat(...songData).map(d => ({ ...d }));
    const csv = d3.csvFormat(concatSongData);
    fs.writeFileSync(`${OUT_PATH}/song-data.csv`, csv)
}

init();