#!/usr/bin/env python3
# file : getKissManagList.py

import cfscrape
import requests
from bs4 import BeautifulSoup as soup


base_url = "http://kissmanga.com"

#Initiate just one scraper and use every where

def create_scraper_new(requests):
    """
    Returns a new scraper instance
    """
    session = requests.session()
    scraper = cfscrape.create_scraper(sess=session)

    return scraper

def getchmn(url, scraper):
    """
    Name : get_chapters_of_manga

    Returns the chapter links array for given valid url of the manga

    eg:
        http://kissmanga.com/Sins
        http://kissmanga.com/One-Piece
        http://kissmanga.com/Onepunch-Man
        
    Use getchchlnk() to get all chapter links from a chapter link
    """

    page = scraper.get(url).content

    souped_html = soup(page, "lxml")

    table = souped_html.find("table",{"class":"listing"})
    links = table.findAll("a")

    ch_links = []

    for link in links:
        ch_links.append(base_url + link["href"])
        
    return ch_links

def getchchlnk(ch_url, scraper):
    """
    Name : get_chapter_links_from_a_chapter_link

    Returns the chapter links array for given valid url of some chapter

    eg:
        http://kissmanga.com/Manga/One-Piece/Chapter-897--Pekoms--Cacao-Island-Escape-Plan?id=407905
        http://kissmanga.com/Manga/One-Piece/Chapter-907--The-Empty-Throne?id=424282
        http://kissmanga.com/Manga/Gintama/Lesson-627?id=357852

    Use getchmn() to get all chapter links of manga
    """

    mn_page = "/".join(ch_url.split("/")[:5])

    return getchmn(mn_page, scraper)

if __name__ == "__main__":

    print("Wait for 10 seconds ...")

    scraper = create_scraper_new(requests)

    url = "http://kissmanga.com/Manga/One-Piece/Chapter-906--The-Holy-Land-Mary-Geoise?id=422953"

    list_chapters = getchchlnk(url, scraper)

    print(list_chapters)