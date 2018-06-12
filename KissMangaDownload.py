#!/usr/bin/env python3
# file : download.py

import cfscrape
import requests
import kissV2, getKissMangaLists, downloadManga
import argparse, json, os

#Scraper instance
session = requests.session()
scraper = cfscrape.create_scraper(sess=session)

#For parsing arguments
parser = argparse.ArgumentParser()

parser.add_argument("-cl", "--chapterlink", dest="chapter_link", help="Chapter Link")
parser.add_argument("-ml", "--mangalink", dest="manga_link", help="Manga Link")
parser.add_argument("-m", "--manga", dest="manga_name", help="Manga Name")
parser.add_argument("-a", "--all", dest="all", default=False, help="Use -a True to download all chapters", type=bool)
parser.add_argument("-d", "--dir", dest="directory", default="Downloads", help="Use -d path to change download path default is ./Downloads")
parser.add_argument("-s", "--start", dest="start", default=0,help="Use -s chapter.no to start from chapter.no")
parser.add_argument("-e", "--end", dest="end",help="Use -e chapter.no to end at chapter.no")

args = parser.parse_args()

manga_link = args.manga_link
manga_name = args.manga_name
chapter_link = args.chapter_link
download_all = args.all
outdir = args.directory

if args.manga_name:
    manga_link = "http://kissmanga.com/Manga/" + args.manga_name

if args.manga_link:
    manga_name = manga_link.split("/")[-1]

if args.chapter_link:
    manga_link = "/".join(chapter_link.split("/")[:5])
    manga_name = manga_link.split("/")[-1]

outdir = os.path.join(outdir, manga_name)

if manga_link and download_all:
    
    #All chapters
    #Usage -ml "URL" -a True
    #OR -m "Name of manga" -a True
    print("Wait for 10 secs.. to bypass cloudflare ddos protection..")
    print("Downloading all chapters from " + manga_link + " ...")

    list_chapters, json_data = getKissMangaLists.getchmn(manga_link, scraper)
    
    downloadManga.write_json(json_data, outdir, 'chapters')

    for chapter in json_data:
        images = kissV2.get_img_urls(chapter['link'], scraper)
        
        file_name="%s_%s" % (chapter['chapter'], 'images')
       
        downloadManga.write_json(
            images,
            os.path.join(outdir, chapter['chapter']),
            file_name
        )
        
        downloadManga.download_images_and_create_pdf(
            images,
            os.path.join(outdir, chapter['chapter']),
            chapter['chapter']
        )

elif manga_link and not download_all:
    print("It currently supports downloading all chapters or only one chapter")
    print("Use -cl <chapter_URL> to give a chapterlink and download that chapter")

if chapter_link and download_all and not manga_link:
    
    #All chapters by giving a chapter link
    #Usage -cl "URL" -a True
    print("Wait for 10 secs.. to bypass cloudflare ddos protection..")
    print("Downloading all chapters ....")

    list_chapters, json_data = getKissMangaLists.getchchlnk(chapter_link, scraper)

    downloadManga.write_json(json_data, outdir, 'chapters')

    for chapter in json_data:
        images = kissV2.get_img_urls(chapter['link'], scraper)
        
        file_name="%s_%s" % (chapter['chapter'], 'images')
        

        downloadManga.write_json(
            images,
            os.path.join(outdir, chapter['chapter']),
            file_name
        )

        downloadManga.download_images_and_create_pdf(
            images,
            os.path.join(outdir, chapter['chapter']),
            chapter['chapter']
        )

elif chapter_link and not download_all and not manga_link:
    
    #Single chapter
    #Usage -cl "" only
    print("Wait for 10 secs.. to bypass cloudflare ddos protection..")
    print("Downloading only this chapter " + chapter_link + " ...")

    dec_imgs_lists = kissV2.get_img_urls(chapter_link, scraper)

    print(dec_imgs_lists)
