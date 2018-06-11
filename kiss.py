#!/usr/bin/env python3

import cfscrape #Only py3

from bs4 import BeautifulSoup as soup
import sys, time
from multiprocessing import Process

def scrape_get(url):
    scraper = cfscrape.create_scraper()

    html_text = scraper.get(url).content
    
    souped_html = soup(html_text,"lxml")

    scripts = souped_html.findAll("script")
    print(scripts)

scrape_get("http://kissmanga.com/Manga/Gintama/Lesson-625?id=348047")