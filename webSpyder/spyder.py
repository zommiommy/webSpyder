

from webSpyder import urls_function as uf
from webSpyder.files_function import check_file_existance
from webSpyder.data_strucutre.initialize import initialize_data_structure

import os
import bs4
import json
import logging
import validators
from tqdm import tqdm


class Spyder():

    # Costructor
    #---------------------------------------------------------------------------

    def __init__(self,settings,project=None):
        self.settings = settings
        if project != None:
            self.settings.set_project(project)

        self.filter_functions  = [self.extension_filter]
        self.functionList = []
        self.cost_function = self.default_cost_function
        start_url = self.settings.get_start_url()

        self.initialize_logger()
        self.urls = initialize_data_structure(self.logger,self.settings)

    def initialize_logger(self):
        self.create_needed_folders()
        self.find_identifier()
        # Setup the logger
        self.logger = logging.getLogger(self.settings.get_project().replace(" ",""))
        self.file_handler = logging.FileHandler(self.settings.get_log_path() + self.settings.get_project() + self.settings.get_identifier() + '.log')
        self.formatter = logging.Formatter(self.settings.get_log_format())
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)

        # Enable or disable the logger
        self.logger.disabled = not self.settings.is_log_enabled()

    def find_identifier(self):
        identifier = 0
        while check_file_existance(self.settings.get_log_path() + self.settings.get_project() + str(identifier) + '.log'):
            identifier += 1
        self.settings.set_identifier(str(identifier))

    def __contains__(self,item):
        return item in self.urls

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.urls)

    def __getitem__(self,key):
        return self.urls[key]

    def __setitem__(self,key,value):
        self.urls[key] = value

    def __str__(self):
        return self.get_status()

    # Observers
    #---------------------------------------------------------------------------


    def get_status(self):
        status = "Current Status:\n"
        status += "settings:\n%s\n"%self.settings
        status += "urls:\n%s"%self.urls
        return status

    def get_settings(self):
        return self.settings

    def get_urls(self):
        return self.urls


    # Modifiers
    #---------------------------------------------------------------------------

    def set_filter(self,f):
        if not callable(f):
            raise Exception("set_filter except a function but the parameter passed is %s"%type(f))

        self.filter_functions.append(f)

    def set_function(self,f):
        if not callable(f):
            raise Exception("set_function except a function but the parameter passed is %s"%type(f))

        self.functionList.append(f)

    def set_cost_function(self,f):
        if not callable(f):
            raise Exception("set_function except a function but the parameter passed is %s"%type(f))

        self.cost_function = f


    # Main methods
    #---------------------------------------------------------------------------

    def create_needed_folders(self):
        cp = self.settings.get_cache_path()
        if not os.path.isdir(cp):
            os.mkdir(cp)

        lp = self.settings.get_log_path()
        if self.settings.is_log_enabled() and not os.path.isdir(lp):
            os.mkdir(lp)

        sp = self.settings.get_state_path()
        if not os.path.isdir(sp):
            os.mkdir(sp)


    def default_cost_function(self,soup,link):
        return 1

    def extension_filter(self,url):
        if self.settings.is_skip_estensions_enabled():
            extension = url.split(".")[-1]
            for ext in self.settings.get_not_skip_estensions_list():
                if  extension.lower() == ext.lower():
                    return False
        return True

    def _url_filer(self,url):
        for ffilter in self.filter_functions:
            result = ffilter(url)
            if result == False:
                return False

        return True

    #---------------------------------------------------------------------------

    #---------------------------------------------------------------------------

    def normalize_links(self,links,url):
        for i,link in enumerate(links):
            links[i] = uf.url_normalize(link,url)
        return links

    def add_link_to_urls(self,father,link):
            self.urls.add_node(father,link)

    def parse_links(self,soup,url):

        links = uf.get_links(soup)

        # construct relative urls
        links = self.normalize_links(links,url)

        # add only valid urls that are not already in list and won't be filtered out
        for link in uf.links_not_in_urls(self.urls,links):
            try:
                #if a valid link and it has not to be filtered
                if validators.url(link) and self._url_filer(link):
                    self.add_link_to_urls(url,link)
            #if everything goes bad the url is not valid
            except ValidationFailure:
                self.logger.warning("Found a non valid url %s"%link)

    def check_and_parse(self,url):
        if self._url_filer(url):
            soup = uf.get_page(url,self.settings,self.logger)

            # Update the cost of the node
            cost = self.cost_function(soup,url)
            self.urls.set_and_update_cost(url,cost)

            # Get the links into the graph
            self.parse_links(soup,url)

            # Call the user functions
            for function in self.functionList:
                function(soup,url)

    def permissive_check_and_parse(self,url):
        try:
            self.check_and_parse(url)
        except Exception as e:
            self.logger.error("ERROR At the iteration over %s"%url)
            self.logger.error(str(e))

    def iteration(self):
        url = self.urls.get_next_page()

        self.logger.info("current url: %s"%url)

        if url == None:
            return False

        if self.settings["permessive_exception"]:
            self.permissive_check_and_parse(url)
        else:
            self.check_and_parse(url)

        return True

    def next(self):
            flag = self.iteration()
            if flag == False:
                raise StopIteration()

    def run(self,num_of_iteration=None):
        if num_of_iteration == None:
            pbar = tqdm()

            flag = True
            try:
                while flag:
                    flag = self.iteration()
                    pbar.update(1)
            except KeyboardInterrupt:
                print("Stopping")

            pbar.close()
        else:
            try:
                r = range(num_of_iteration)

                if self.settings.is_tqdm_run_enabled():
                    r = tqdm(r)

                for i in r:
                    flag = self.iteration()
                    if flag == False:
                        break
            except KeyboardInterrupt:
                print("Stopping")
