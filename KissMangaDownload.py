#!/usr/bin/env python3
# file : download.py

import cfscrape
import requests
import kissV2, getKissMangaLists, downloadManga
import argparse, json, os

base_url = "http://kissmanga.com/Manga/"

#Scraper instance
session = requests.session()
scraper = cfscrape.create_scraper(sess=session)

#For parsing arguments
parser = argparse.ArgumentParser()

parser.add_argument("-cl", "--chapterlink", dest="chapter_link", default="", help="Chapter Link")
parser.add_argument("-ml", "--mangalink", dest="manga_link", default="", help="Manga Link")
parser.add_argument("-m", "--manga", dest="manga_name", default="", help="Manga Name")
parser.add_argument("-a", "--all", dest="all", nargs='?', const=True, help="Use -a or --all to download all chapters", type=bool)
parser.add_argument("-d", "--dir", dest="directory", default="Manga", help="Use -d path to change download path default is ./Manga")
parser.add_argument("-s", "--start", dest="start", default=0,help="Use -s chapter.no to start from chapter.no")
parser.add_argument("-e", "--end", dest="end", help="Use -e chapter.no to end at chapter.no")
parser.add_argument("-l", "--list", dest="list_chapters", nargs='?', const=True, help="Lists chapter names", type=bool)

args = parser.parse_args()

manga_link = args.manga_link
manga_name = args.manga_name
chapter_link = args.chapter_link
download_all = args.all
outdir = args.directory

if args.manga_name:
    manga_link = base_url + args.manga_name

if args.manga_link:
    manga_name = manga_link.split("/")[-1]

if args.chapter_link:
    manga_link = "/".join(chapter_link.split("/")[:5])
    manga_name = manga_link.split("/")[-1]

if args.list_chapters and manga_link:

    print("Wait for 10 secs to bypass cloudflare ddos protection ...")
    print("Listing all chapter names of " + manga_link)

    list_chapters, json_data = getKissMangaLists.getchmn(manga_link, scraper)
    
    for chapter in json_data:
        print(chapter['chapter'])

outdir = os.path.join(outdir, manga_name)

if download_all:

    #All chapters
    #Usage -ml "URL" -a True
    #OR -m "Name of manga" -a True
    print("Wait for 10 secs to bypass cloudflare ddos protection ...")
    print("Downloading all chapters from " + manga_link + " ...")

    list_chapters, json_data = getKissMangaLists.getchmn(manga_link, scraper)

    #Make a chapters.json file
    downloadManga.write_json(json_data, outdir, 'chapters')

    downloadManga.download_chapters(json_data, outdir, scraper)

elif manga_link and not chapter_link:
    print("It currently supports downloading all chapters or only one chapter")
    print("Use -cl <chapter_URL> to give a chapterlink and download that chapter")
    print("Or -a to download every chapter")

elif chapter_link:

    #Single chapter
    #Usage -cl "" only
    print("Wait for 10 secs to bypass cloudflare ddos protection ...")
    print("Downloading only this chapter " + chapter_link + " ...")

    dec_imgs_list = kissV2.get_img_urls(chapter_link, scraper)

    details = kissV2.get_chapter_detalis(chapter_link, scraper)

    downloadManga.write_json(
            dec_imgs_list,
            os.path.join(outdir, details['title']),
            details['title'] + "_images"
        )

    downloadManga.download_images_and_create_pdf(
            dec_imgs_list,
            os.path.join(outdir, details['title']),
            details['title']
        )