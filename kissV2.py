#!/usr/bin/env python3
# file : kissV2.py

import cfscrape #Only py3

from bs4 import BeautifulSoup as soup
import sys, time, re, os, ast

import subprocess

def scrape_get_scripts(url):
    """Returns script array from the webpage"""
    scraper = cfscrape.create_scraper()
    html_text = scraper.get(url).content
    souped_html = soup(html_text,"lxml")
    scripts = souped_html.findAll("script")
    return scripts



def get_ecrypted_links(sc_array):
    """Returns encrypted img-links from given script array"""    
    #I'm accessing the 11th element from scripts array from beautifulsoup
    #Need to think of a better way of accessing

    #ex:
    #Like get only script tags with no src attributes
    # this will slightly decrease the space complexicity

    script_final = sc_array[10]

    #This gives all the encrypted links like grep
    results = re.findall(r'lstImages.push\(wrapKA\("(.*)"\)\);', str(script_final.text))

    return results


def get_decrypted_imgs(enc_array):
    """Returns the decrypted array of image-links for given ecrypted-arry (enc_array)"""
    with open("temp.js", "w+") as temp_file:
        with open("index.js" , "r") as file_js:
            for line in file_js:
                temp_file.write(line)
        
        temp_file.write("var lstImages = [ \n")

        for a in enc_array:
            temp_file.write("wrapKA(\"" + a + "\"),\n")
        
        temp_file.write("];\n")

        temp_file.write("console.log(lstImages);")

    #execute the temp.js using node and subprocess and delete it
    output = subprocess.check_output(["node", "temp.js"])
    os.remove("temp.js")

    #bytes to string
    output = output.decode("utf-8")

    #This is dangerous
    list_imgs = ast.literal_eval(output)

    return list_imgs


sc_array = scrape_get_scripts("http://kissmanga.com/Manga/Gintama/Lesson-625?id=348047")

enc_array = get_ecrypted_links(sc_array)

img_links = get_decrypted_imgs(enc_array)

print(img_links)