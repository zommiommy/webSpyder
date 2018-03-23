
from . import get_page_methods
from . import files_function

import bs4
import os
import string
from urllib.parse import urljoin

def url_normalize(link,url):
    # join the url and the father so if it is a relative link it get resolved to absolute
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

def page_download(url,mode,name,directory,logger):
    # aviable download modes
    modes = {
        "wget":get_page_methods.wget.wget_get_page,
        #"urllib":get_page_methods.urllib.urllib_get_page,
        #"selenium":get_page_methods.selenium.selenium_get_page,
        #"requests":get_page_methods.requests.requests_get_page
    }
    # check if the mode is avaiable
    if mode in modes.keys():
        # if it is call it
        logger.info("downloading using %s mode"%mode)
        modes[mode](url,name,directory,logger)
    else:
        # else raise an exception
        logger.info('Unkown get_page mode %s the aviable one are %s'%(mode,modes.keys()))
        raise Exception('Unkown get_page mode %s the aviable one are %s'%(mode,modes.keys()))

def get_soup_and_html(url,mode,name,directory,logger):
    name = "temp.html"
    # if there isen't download it
    page_download(url,mode,name,directory,logger)

    html = files_function.read_file("%s%s"%(directory,name))

    soup = bs4.BeautifulSoup(html, "lxml")

    return soup,html


def get_page(url,settings,logger):

    mode, cache, directory = settings["mode"], settings["cache"], settings["cache_path"]

    if cache == False:
        # just download the page
        logger.info("just downloading %s"%url)
        soup,html = get_soup_and_html(url,mode,name,directory,logger)
        return soup

    # Else if cache == True
    name = hash_url(url) + ".html"
    # check if the page is already downloaded
    if  name in os.listdir(directory):
        # if the page was already downloaded use it
        logger.info("using cached %s"%name)
        html = files_function.read_file("%s%s"%(directory,name))
        return bs4.BeautifulSoup(html, "lxml")
    else:

        logger.info("no cache found so it has to be downloaded, %s"%url)
        # if there the page is note there download it
        soup,html = get_soup_and_html(url,mode,name,directory,logger)

        # if it has to be cleared clear it
        if settings["clear_html"] == True:
            # Clear the soup
            soup = clear_useless_stuff(soup,settings)
            # Remove White Spaces
            html = remove_white_spaces(soup)
            logger.info("cleared %s"%name)
        # else/then write the file

        # Write the file
        name = hash_url(url) + ".html"
        with open("%s%s"%(directory,name),"w") as f:
            f.write(html)

        logger.info("written %s"%name)

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

def remove_white_spaces(soup):
    html = str(soup)
    html = "".join(line.strip() for line in html.split("\n"))
    return html

def clear_useless_stuff(soup,settings):
    # Remove all the comments
    if settings["clear_comments"] == True:
        soup = remove_comments_from_soup(soup)

    # Remove useless tag
    soup = remove_useless_tags(soup,settings)

    # Remove useless attributes
    soup = remove_useless_attributes(soup,settings)

    return soup
