#!/usr/bin/env python3
# file : kissV2.py

import cfscrape #Only py3
import requests
from bs4 import BeautifulSoup as soup
import sys, re, os, ast
import subprocess

def scrape_get_scripts(urls = []):
    """
    Returns script lists from the webpages of all urls given
    
    First url takes 10 seconds and others will be immediate
    """
    #The advantage is to use the same cfscrape instance to get all the urls
    #It would be useless if we have to wait for 10 secs for every link
    
    session = requests.session()
    scraper = cfscrape.create_scraper(sess=session)
    scripts = []
    for url in urls:
        print(url)
        html_text = scraper.get(url).content
        souped_html = soup(html_text,"lxml")
        scripts.append(souped_html.findAll("script"))
    return scripts



def get_ecrypted_links(sc_lists):
    """
    Returns encrypted img-link lists from given script lists
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

if __name__ == "__main__":
    urls = ["http://kissmanga.com/Manga/Gintama/Lesson-627?id=357852",
            "http://kissmanga.com/Manga/Gintama/Lesson-625?id=348047",
            "http://kissmanga.com/Manga/Gintama/Lesson-628?id=359062",
            "http://kissmanga.com/Manga/Gintama/Lesson-629?id=359699",
            "http://kissmanga.com/Manga/One-Piece/Chapter-907--The-Empty-Throne?id=424282",
            "http://kissmanga.com/Manga/One-Piece/Chapter-906--The-Holy-Land-Mary-Geoise?id=422953",
            "http://kissmanga.com/Manga/One-Piece/885---It-s-Brulee-?id=390134"]

    print("Wait for 10 secs ...")
    sc_lists = scrape_get_scripts(urls)

    enc_lists = get_ecrypted_links(sc_lists)

    img_link_lists = get_decrypted_imgs(enc_lists)

    print(img_link_lists)