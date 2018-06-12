#!/usr/bin/env python3
# file : download.py

import cfscrape
import requests
import kissV2, getKissMangaLists
import argparse

#Scraper instance
session = requests.session()
scraper = cfscrape.create_scraper(sess=session)

#For parsing arguments
parser = argparse.ArgumentParser()

parser.add_argument("-cl", "--chapterlink", dest="chapter_link", help="Chapter Link")
parser.add_argument("-ml", "--mangalink", dest="manga_link", help="Manga Link")
parser.add_argument("-m", "--manga", dest="manga_name", help="Manga Name")
parser.add_argument("-a", "--all", dest="all", default=False, help="Use -a True to download all chapters", type=bool)

args = parser.parse_args()

manga_link = None
chapter_link = None
download_all = args.all

if args.manga_name:
    manga_link = "http://kissmanga.com/Manga/" + args.manga_name

if args.manga_link:
    manga_link = args.manga_link

if args.chapter_link:
    chapter_link = args.chapter_link



if manga_link and download_all:
    
    #All chapters
    #Usage -ml "URL" -a True
    #OR -m "Name of manga" -a True
    print("Wait for 10 secs.. to bypass cloudflare ddos protection..")
    print("Downloading all chapters from " + manga_link + " ...")

    list_chapters = getKissMangaLists.getchmn(manga_link, scraper)
    sc_lists = kissV2.scrape_get_scripts(scraper, urls=list_chapters)
    enc_lists = kissV2.get_encrypted_links(sc_lists)
    dec_imgs_lists = kissV2.get_decrypted_imgs(enc_lists)

    print(dec_imgs_lists)

elif manga_link and not download_all:
    print("It currently supports downloading all chapters or only one chapter")
    print("Use -cl <chapter_URL> to give a chapterlink and download that chapter")

if chapter_link and download_all and not manga_link:
    
    #All chapters by giving a chapter link
    #Usage -cl "URL" -a True
    print("Wait for 10 secs.. to bypass cloudflare ddos protection..")
    print("Downloading all chapters ....")

    list_chapters = getKissMangaLists.getchchlnk(chapter_link, scraper)
    sc_lists = kissV2.scrape_get_scripts(scraper, urls=list_chapters)
    enc_lists = kissV2.get_encrypted_links(sc_lists)
    dec_imgs_lists = kissV2.get_decrypted_imgs(enc_lists)

    print(dec_imgs_lists)

elif chapter_link and not download_all and not manga_link:
    
    #Single chapter
    #Usage -cl "" only
    print("Wait for 10 secs.. to bypass cloudflare ddos protection..")
    print("Downloading only this chapter " + chapter_link + " ...")

    list_chapters = [chapter_link]
    sc_lists = kissV2.scrape_get_scripts(scraper, urls=list_chapters)
    enc_lists = kissV2.get_encrypted_links(sc_lists)
    dec_imgs_lists = kissV2.get_decrypted_imgs(enc_lists)

    print(dec_imgs_lists)
