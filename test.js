const puppeteer = require('puppeteer');
// const prompt = require("prompts");
// const fs = require('fs-extra');

const screenshot = 'immo.png';
var state = "berlin";
var city = "berlin";
var page_num = 1;
var website = "https://www.immobilienscout24.de/Suche/de/"+state+"/"+city+"/wohnung-mieten?pagenumber="+page_num;

// IIFE
(async() => {

    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    await page.goto(website);
    // await page.type('#txEmail', userData.user);
    // await page.type('#txPassword', userData.password);
    // await page.click('#btnLogin');
    await page.waitForNavigation();
    // await page.goto(bcPastWorkouts);
    var htmlContent = await page.content();
    await page.screenshot({ path: screenshot });
    browser.close();
    console.log('See screenshot: ' + screenshot);

})();