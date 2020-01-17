const fs = require('fs');
const d3 = require('d3');
const request = require('request');

const OUT_PATH = './output'
const YEARS = d3.range(2006, 2020)
const BASE_URL_START = 'https://www.billboard.com/charts/year-end/'
const BASE_URL_END = '/hot-100-songs'

async function getBillboardHTML(year) {
    const COMPLETE_URL = `${BASE_URL_START}${year}${BASE_URL_END}`

    return new Promise((resolve, reject) => {
        request(COMPLETE_URL, (err, response, body) => {
            fs.writeFileSync(`${OUT_PATH}/billboard-${year}.html`, body)
        })
    })
}

function init() {
    YEARS.map(getBillboardHTML);
}

init();