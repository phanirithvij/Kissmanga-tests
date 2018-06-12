#!/usr/bin/env python3
# file : getKissManagList.py

import cfscrape, re
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

    Usage: return_value[0] contains the list 

    Returns the chapter links list and a json data for given valid url of the manga

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

    data_for_json = []

    for link in links:

        url_chapter = base_url + link["href"]
        ch_links.append(url_chapter)

        data_for_json.append({
            "chapter": re.sub('[^\w\s-]', '', link.get_text().strip().replace(':', " -")),
            "link": url_chapter
        })
    
    return (ch_links, data_for_json)

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

    list_chapters, data = getchchlnk(url, scraper)

    print(list_chapters)