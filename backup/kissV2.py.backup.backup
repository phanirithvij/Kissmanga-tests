#!/usr/bin/env python3
# file : kissV2.py

import cfscrape #Only py3
import requests
from bs4 import BeautifulSoup as soup
import sys, re, os, ast
import subprocess


def create_scraper_new(requests):
    """
    Returns a new scraper instance
    """
    session = requests.session()
    scraper = cfscrape.create_scraper(sess=session)

    return scraper


def scrape_get_scripts(scraper, urls = []):
    """
    Returns script lists from the webpages of all urls given
    
    First url takes 10 seconds and others will be immediate

    scraper is passed because:
    
    The advantage is to use the same cfscrape instance to get all the urls
    It would be useless if we have to wait for 10 secs for every link
    
    """

    scripts = []
    for url in urls:
        print(url)
        html_text = scraper.get(url).content
        souped_html = soup(html_text,"lxml")
        scripts.append(souped_html.findAll("script"))
    return scripts



def get_encrypted_links(sc_lists):
    """
    Returns encrypted img-link lists from given script lists

    Uses python re module
    """
    
    #I'm accessing the 11th element from scripts list from beautifulsoup
    #Need to think of a better way of accessing

    #ex:
    #Like get only script tags with no src attributes
    # this will slightly decrease the space complexicity
    results = []

    for sc_list in sc_lists:
        script_final = sc_list[10]

        #This gives all the encrypted links like grep
        results.append(re.findall(r'lstImages.push\(wrapKA\("(.*)"\)\);', str(script_final.text)))

    return results


def get_decrypted_imgs(enc_lists):
    
    """
    Returns the decrypted lists of image-links for given ecrypted-lists (enc_lists)

    Uses node js and index.js must exist in the current directory
    """
    
    list_imgs = []
    for enc_list in enc_lists:

        with open("temp.js", "w+") as temp_file:
            with open("index.js" , "r") as file_js:
                for line in file_js:
                    temp_file.write(line)
            
            temp_file.write("var lstImages = [ \n")

            for a in enc_list:
                temp_file.write("wrapKA(\"" + a + "\"),\n")
            
            temp_file.write("];\n")

            temp_file.write("console.log(lstImages);")

        #execute the temp.js using node and subprocess and delete it
        output = subprocess.check_output(["node", "temp.js"])
        os.remove("temp.js")

        #bytes to string
        output = output.decode("utf-8")

        #This is dangerous
        list_imgs.append(ast.literal_eval(output))

    return list_imgs

def get_img_urls(chapter_url, scraper):
    """
    Returns list of images of a chapter
    """

    list_scripts = scrape_get_scripts(scraper, urls=[chapter_url])
    enc_lists = get_encrypted_links(list_scripts)
    imgs_lists = get_decrypted_imgs(enc_lists)

    return imgs_lists[0]

def get_chapter_detalis(chapter_url, scraper):
    """
    Returns chapter details of a particular chapter

    {
        title,
        chapter_no,
        date
    }
    """
    chapter_no = None
    title = ""
    date = ""
    
    manga_link = "/".join(chapter_url.split("/")[:5])
    html_text = scraper.get(manga_link).content
    souped_html = soup(html_text,"lxml")


    table = souped_html.find("table",{"class":"listing"})
    links = table.findAll("tr")


    json_data = []

    index = 1

    for link in links:
        cells = link.findAll("td")
        if not cells:
            continue

        a_tag = cells[0].find("a")

        url_chapter = "http://kissmanga.com" + a_tag["href"]

        json_data.append({
            "title": re.sub('[^\w\s-]', '', a_tag.get_text().strip().replace(':', " -")),
            "link": url_chapter,
            "date": cells[1].get_text(),
            "pos":index
        })
        index += 1

    for chapter in json_data:
        if chapter['link'] == chapter_url:
            title = chapter['title']
            chapter_no = index - chapter['pos']
            date = chapter['date']

    return {
            "title" : title,
            "chapter_no" : chapter_no,
            "date": date    
    }

if __name__ == "__main__":
    urls = ["http://kissmanga.com/Manga/Gintama/Lesson-627?id=357852",
            "http://kissmanga.com/Manga/Gintama/Lesson-625?id=348047",
            "http://kissmanga.com/Manga/Gintama/Lesson-628?id=359062",
            "http://kissmanga.com/Manga/Gintama/Lesson-629?id=359699",
            "http://kissmanga.com/Manga/One-Piece/Chapter-907--The-Empty-Throne?id=424282",
            "http://kissmanga.com/Manga/One-Piece/Chapter-906--The-Holy-Land-Mary-Geoise?id=422953",
            "http://kissmanga.com/Manga/One-Piece/885---It-s-Brulee-?id=390134"]

    print("Wait for 10 secs ...")

    scraper = create_scraper_new(requests)

    for url in urls:
        a = get_img_urls(url, scraper)
        print(a)