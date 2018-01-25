
import webSpyder.helper_functions as hf
import webSpyder.helper_functions.urls_function as uf
import bs4
from tqdm import tqdm

from . import __path__ as package_path

def is_not_function(f):
    return str(type(f)) != "<class 'function'>"


class Spyder():

    settings = {
        "mode":"wget",
        "start_url":"",
        "directory":"%s/pagecaches/"%package_path[0],
        "cache":True
    }

    def __init__(self,start_url):
        self.settings["start_url"] = start_url
        self.filter_functions  = []
        self.functionList = []
        self.urls, self.index = [start_url] , 0

    def __str__(self):
        return "settings:\n%s\n\nindex: %s\n\nurls:\n%s"%(self.settings,self.index,self.urls)

    def _url_filer(self,url):
        for filter in self.filter_functions:
            result = filter(url)
            if result == False:
                return False

        return True

    def set_filter(self,f):
        if is_not_function(f):
            raise Exception("set_filter except a function but the parameter passed is %s"%type(f))

        self.filter_functions.append(f)

    def set_function(self,f):
        if is_not_function(f):
            raise Exception("set_function except a function but the parameter passed is %s"%type(f))

        self.functionList.append(f)

    def iteration(self):
        url = self.urls[self.index]
        print(url)

        if self._url_filer(url):
            html = uf.get_page(url,self.settings)

            soup = bs4.BeautifulSoup(html, "lxml")

            for function in self.functionList:
                function(soup,url)

            links = uf.get_links(soup)

            for link in uf.links_not_in_urls(self.urls,links):
                self.urls.append(uf.url_normalize(link,url))

        self.index += 1

    def run(self):
        pbar = tqdm()
        while self.index < len(self.urls):
            self.iteration()
            pbar.update(1)
        pbar.close()

