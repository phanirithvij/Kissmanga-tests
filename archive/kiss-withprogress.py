import cfscrape
from bs4 import BeautifulSoup as soup
import sys, time
from multiprocessing import Process

def scrape_get():
    scraper = cfscrape.create_scraper()

    html_text = scraper.get("http://kissmanga.com/Manga/Gintama/Lesson-625?id=348047").content
    
    souped_html = soup(html_text,"lxml")

    scripts = souped_html.findAll("script")
    print(scripts)

def count_secs():
    for count in range(11):
        done = count * 5
        sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
        sys.stdout.flush()
        time.sleep(1)

p1 = Process(target=scrape_get)
p2 = Process(target=count_secs)

p1.start()
p2.start()

p1.join()
p2.join()

