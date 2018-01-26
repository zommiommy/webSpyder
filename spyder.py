
import webSpyder.helper_functions as hf
import webSpyder.helper_functions.urls_function as uf
import bs4
import logging
from tqdm import tqdm
from . import __path__ as package_path

# Horrible workaround, TODO do it in the right way
def is_not_function(f):
    return str(type(f)) != "<class 'function'>"


class Spyder():

    settings = {
        "mode":"wget",
        "start_url":"",

        "cache":True,
        "cache_path":"%s/pagecaches/"%package_path[0],

        "log": True,
        "log_path":"%s/log/"%package_path[0],
        "log_format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    # Costructor
    #---------------------------------------------------------------------------

    def __init__(self,start_url):
        self.settings["start_url"] = start_url
        self.filter_functions  = []
        self.functionList = []
        self.urls, self.index = [start_url] , 0

        # Setup the logger
        self.logger = logging.getLogger('webSpyder')
        self.file_handler = logging.FileHandler(self.settings["log_path"] + 'spyder.log')
        self.formatter = logging.Formatter(self.settings["log_format"])
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)

        # Enable or disable the logger
        self.logger.disabled = not self.settings["log"]


    # Observers
    #---------------------------------------------------------------------------

    def __str__(self):
        return self.get_status()

    def get_status(self):
        status = "Current Status:\n"
        status += "settings:\n%s\n"%self.settings
        status += "index: %s\n"%self.index
        status += "urls:\n%s"%self.urls
        return status

    def get_settings(self):
        return self.settings

    def get_index(self):
        return self.index

    def get_urls(self):
        return self.urls


    # Modifiers
    #---------------------------------------------------------------------------

    def set_filter(self,f):
        if is_not_function(f):
            raise Exception("set_filter except a function but the parameter passed is %s"%type(f))

        self.filter_functions.append(f)

    def set_function(self,f):
        if is_not_function(f):
            raise Exception("set_function except a function but the parameter passed is %s"%type(f))

        self.functionList.append(f)

    # Settings Modifiers
    #---------------------------------------------------------------------------

    def set_mode(self,value):
        self.settings["mode"] = value

    def set_start_url(self,value):
        self.settings["start_url"] = value
        self.urls.append(value)

    def set_cache(self,value):
        self.settings["cache"] = value

    def set_cache_path(self,value):
        self.settings["cache_path"] = value

    def set_log(self,value):
        self.settings["log"] = value

    def set_log_path(self,value):
        self.settings["log_path"] = value

    def set_log_format(self,value):
        self.settings["log_format"] = value



    # Main methods
    #---------------------------------------------------------------------------

    def _url_filer(self,url):
        for filter in self.filter_functions:
            result = filter(url)
            if result == False:
                return False

        return True

    def iteration(self):
        url = self.urls[self.index]
        self.logger.info("current url: %s"%url)

        if self._url_filer(url):
            html = uf.get_page(url,self.settings,self.logger)

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

