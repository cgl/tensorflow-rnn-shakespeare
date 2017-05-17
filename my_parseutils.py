from urllib.request import urlopen
from bs4 import BeautifulSoup
import os, unicodedata, re

def slugify(value):
    """
    Converts to lowercase, removes non-word characters (alphanumerics and
    underscores) and converts spaces to hyphens. Also strips leading and
    trailing whitespace.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)

def fetch_page(url):
    response = urlopen(url) ; page = BeautifulSoup(response.read(),"html.parser")
    return page


def write_to_file(url):
    page = fetch_page(url)
    title = page.find("span", {'itemprop':"itemReviewed"}).getText()
    text = page.find("div", {'class': "text"}).getText()
    filename = os.path.join("masal", url.split("/")[-1] + ".txt")
    with open(filename,"w",encoding="utf-8") as out:
        print("%s\n%s" %(title,text), file=out)

def get_stories():
    main_url = "http://www.grimmstories.com/tr/grimm_masallari/list"
    page = fetch_page(main_url)

    urls_div = page.find("div", {'class': "main"})
    urls = []
    for li in urls_div.find_all("li"):
        url = li.a.get('href')
        write_to_file(url)

