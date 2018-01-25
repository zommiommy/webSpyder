
from . import get_page_methods
from . import files_function
import string
import os

def url_normalize(link,url):
    if link.startswith("/"):
        if url.endswith("/"):
            return url + link
        else:
            return url + "/" + link
    else:
        return link


def get_links(soup):
    results = soup.find_all("a")
    links = []
    for link in results:
        try:
            links.append(link["href"])
        except:
            pass
    return links


def url_filer(url):
    if url == "" or url == None:
        return False

    if black_list != []:
        for el in black_list:
            if el != None and el in url:
                print("B ",end="")
                return False

    if white_list != []:
        for el in white_list:
            if  el != None and el not in url:
                print("W ",end="")
                return False

    return True



def links_not_in_urls(urls,links):
    return filter(lambda x: x if x not in urls else None,links)

def hash_url(url):
    new_url = ""
    for character in url:
        if character in string.ascii_letters:
            new_url += character

    return new_url

def get_page(url,settings):

    mode      = settings["mode"]
    directory = settings["directory"]
    cache     = settings["cache"]

    if cache == True:
        name = hash_url(url) + ".html"
        if  name in os.listdir(directory):
            print("using cached %s"%name)
            return files_function.read_file("%s%s"%(directory,name))
    else:
        name = "tmp.html"


    if mode == "wget":
        get_page_methods.wget.wget_get_page(url,name,directory)

    elif mode == "urllib":
        get_page_methods.urllib.urllib_get_page(url,name,directory)

    elif mode == "selenium":
        get_page_methods.selenium.selenium_get_page(url,name,directory)
        pass
    elif mode == "requests":
        get_page_methods.requests.requests_get_page(url,name,directory)
    else:
        raise Exception('Unkown get_page mode %s the aviable one are wget,urllib,selenium,requests'%mode)

    return files_function.read_file("%s%s"%(directory,name))
