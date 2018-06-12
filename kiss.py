#!/usr/bin/env python3
# file : kiss.py

import cfscrape #Only py3

from bs4 import BeautifulSoup as soup
import sys, time, re, os, json, ast

import subprocess

def scrape_get(url):
    """Returns script array from the webpage"""
    scraper = cfscrape.create_scraper()
    html_text = scraper.get(url).content
    souped_html = soup(html_text,"lxml")
    scripts = souped_html.findAll("script")
    return scripts

sc_array = scrape_get("http://kissmanga.com/Manga/Gintama/Lesson-625?id=348047")

#print(len(sc_array))

script_final = ""

#for s in sc_array:
 #   if "lstImages" in s.string:
  #      script_final = s
   #     print(script_final)

#I'm accessing the 11th element from scripts array from beautifulsoup
#Need to think of a better way of accessing

#ex:
#Like get only script tags with no src attributes
# this will slightly decrease the space complexicity

script_final = sc_array[10]


#This gives all the encrypted links like grep
results = re.findall(r'lstImages.push\(wrapKA\("(.*)"\)\);', str(script_final.text))

#START

    #IMPORTANT
    #TODO(Not a todo but it's important)

    #http://kissmanga.com/Scripts/lo.js
    #http://kissmanga.com/Scripts/ca.js

    #and crypto-js npm are in index.js which is used as the heart for the decryption of the image links 

#END

with open("temp.js", "w+") as temp_file:


    with open("index.js" , "r") as file_js:

        for line in file_js:
            temp_file.write(line)
    
    temp_file.write("lstImages = [")

    for a in results:
        temp_file.write("wrapKA(\"" + a + "\"),")
    
    temp_file.write("];")

    temp_file.write("console.log(lstImages);")


#execute the temp.js using node and subprocess
output = subprocess.check_output(["node", "temp.js"])
os.remove("temp.js")

#bytes to string
output = output.decode("utf-8")

#This is dangerous
list_imgs = ast.literal_eval(output)

print(list_imgs)