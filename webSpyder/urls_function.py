
from . import get_page_methods
from . import files_function

import bs4
import os
import string
from urllib.parse import urljoin

def url_normalize(link,url):
        return urljoin(url,link)


def get_links(soup):
    results = soup.find_all("a")
    links = []
    for link in results:
        try:
            links.append(link["href"])
        except:
            pass
    return links




def links_not_in_urls(urls,links):
    return filter(lambda x: x if x not in urls else None,links)

def hash_url(url):
    new_url = ""
    for character in url:
        if character in string.ascii_letters:
            new_url += character

    return new_url

def get_page(url,settings,logger):

    mode      = settings["mode"]
    cache     = settings["cache"]
    directory = settings["cache_path"]

    if cache == True:
        name = hash_url(url) + ".html"
        if  name in os.listdir(directory):
            logger.info("using cached %s"%name)
            return files_function.read_file("%s%s"%(directory,name))
    else:
        name = "tmp.html"


    if mode == "wget":
        get_page_methods.wget.wget_get_page(url,name,directory,logger)

    elif mode == "urllib":
        get_page_methods.urllib.urllib_get_page(url,name,directory,logger)

    elif mode == "selenium":
        get_page_methods.selenium.selenium_get_page(url,name,directory,logger)
        pass
    elif mode == "requests":
        get_page_methods.requests.requests_get_page(url,name,directory,logger)
    else:
        raise Exception('Unkown get_page mode %s the aviable one are wget,urllib,selenium,requests'%mode)

    html = files_function.read_file("%s%s"%(directory,name))

    soup = bs4.BeautifulSoup(html, "lxml")

    # Clear the soup
    if settings["clear_html"] == True:
        soup = clear_useless_stuff(soup)

    return soup


    def remove_comments_from_soup(soup):
        comments = soup.findAll(text=lambda text:isinstance(text, bs4.Comment))
        for comment in comments:
            comment.extract()
        return soup

    def remove_useless_tags(soup,settings):
        for tag in settings["useless_tags"]:
            for item in soup(tag):
                item.decompose()
        return soup

    def remove_useless_attributes(soup,settings):
        for tag in soup():
            for attribute in settings["useless_attributes"]:
                del tag[attribute]
        return soup

    def remove_white_spaces(soup,settings):
        html = str(soup)
        html = "".join(line.strip() for line in html.split("\n"))
        soup = bs4.BeautifulSoup(html, "lxml")
        return soup

    def clear_useless_stuff(soup,settings):
        # Remove all the comments
        if settings["clear_comments"] == True:
            soup = remove_comments_from_soup(soup,settings)

        # Remove useless tag
        soup = remove_useless_tags(soup,settings)

        # Remove useless attributes
        soup = remove_useless_attributes(soup,settings)

        # Remove White Spaces
        soup = remove_white_spaces(soup,settings)

        return soup
