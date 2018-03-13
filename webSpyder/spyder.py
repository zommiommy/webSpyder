
from . import urls_function as uf

import os
import bs4
import json
import logging
import validators
from . import linkGraph
from tqdm import tqdm

# Horrible workaround TODO find a not stupid way
from . import __path__ as package_path

# Horrible workaround part 2, TODO do it in the right way
def is_not_function(f):
#    return str(type(f)) != "<class 'function'>"
    return type(f) != type(lambda x: x)

class Spyder():

    settings = {
        "data_type":"list",
        "mode":"wget",
        "permessive_exception":True,
        "start_url":"",
        "project":"webSpyder",

        "clear_html":False,
        "clear_comments":True,
        "useless_tags":["svg","input","noscript","link","script","style","iframe","canvas"],
        "useless_attributes":["style", "href", "role", "src","target","type","lang","async","crossorigin"],

        "skip_estensions":True,
        "not_skip_estensions_list":["html","htm","php","aspx","asp","axd","asx","asmx","ashx","cfm","xml","rss","cgi","jsp","jspx",],

        "cache":False,
        "cache_path":"%s/pagecaches/"%os.getcwd(),

        "log": True,
        "log_path":"%s/log/"%os.getcwd(),
        "log_format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    # Costructor
    #---------------------------------------------------------------------------

    def __init__(self,project=None):
        if project != None:
            self.settings["project"] = project

        self.filter_functions  = [self.extension_filter]
        self.functionList = []
        self.cost_function = self.default_cost_function
        start_url = self.settings["start_url"]

        self.initialize_logger()

        self.update_data_structure()

    def initialize_logger(self):
        self.create_needed_folders()
        # Setup the logger
        self.logger = logging.getLogger(self.settings["project"].replace(" ",""))
        self.file_handler = logging.FileHandler(self.settings["log_path"] + self.settings["project"] + '.log')
        self.formatter = logging.Formatter(self.settings["log_format"])
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)

        # Enable or disable the logger
        self.logger.disabled = not self.settings["log"]

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
        status += "settings:\n%s\n"%json.dumps(self.settings, indent=4)
        status += "urls:\n%s"%self.urls
        return status

    def get_settings(self):
        return self.settings

    def get_urls(self):
        return self.urls

    def get_useless_tags(self):
        return self.settings["useless_tags"]

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

    def set_cost_function(self,f):
        if is_not_function(f):
            raise Exception("set_function except a function but the parameter passed is %s"%type(f))

        self.cost_function = f


    def set_useless_attributes(self,attributes):
        self.settings["useless_attributes"] = attributes
        self.enable_clear_html()

    def set_useless_tags(self,tags):
        self.settings["useless_tags"] += tags
        self.enable_clear_html()

    # Settings Modifiers
    #---------------------------------------------------------------------------

    def enable_permessive_exception(self):
        self.settings["permessive_exception"] = True
    def disable_permessive_exception(self):
        self.settings["permessive_exception"] = False

    def enable_clear_html(self):
        self.settings["clear_html"] = True
    def disable_clear_html(self):
        self.settings["clear_html"] = False

    def enable_clear_comments(self):
        self.settings["clear_comments"] = True
    def disable_clear_comments(self):
        self.settings["clear_comments"] = False

    def enable_cache(self):
        self.settings["cache"] = True
    def disable_cache(self):
        self.settings["cache"] = False

    def enable_log(self):
        self.settings["log"] = True
    def disable_log(self):
        self.settings["log"] = False


    def set_mode(self,value):
        self.settings["mode"] = value

    def set_data_type(self,value):
        self.settings["data_type"] = value
        self.update_data_structure()

    def set_start_url(self,value):
        self.settings["start_url"] = value
        self.update_data_structure()
        self.urls.add_root(value)

    def set_cache_path(self,value):
        self.settings["cache_path"] = value

    def set_log_path(self,value):
        self.settings["log_path"] = value

    def set_log_format(self,value):
        self.settings["log_format"] = value



    # Main methods
    #---------------------------------------------------------------------------

    def update_data_structure(self):
        if self.settings["data_type"] == "list":
            self.logger.info("Starting with list data structure")
            self.urls = WebList(self.logger)
        else:
            self.logger.info("Starting with graph data structure")
            self.urls = linkGraph.linkGraph(self.logger)

    def create_needed_folders(self):
        cp = self.settings["cache_path"]
        if not os.path.isdir(cp):
            os.mkdir(cp)

        lp = self.settings["log_path"]
        if self.settings["log"] and not os.path.isdir(lp):
            os.mkdir(lp)

    def default_cost_function(self,soup,link):
        return 1

    def extension_filter(self,url):
        if self.settings["skip_estensions"]:
            extension = url.split(".")[-1]
            for ext in self.settings["not_skip_estensions_list"]:
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
    def remove_comments_from_soup(self,soup):
        comments = soup.findAll(text=lambda text:isinstance(text, bs4.Comment))
        for comment in comments:
            comment.extract()
        return soup

    def remove_useless_tags(self,soup):
        for tag in self.settings["useless_tags"]:
            for item in soup(tag):
                item.decompose()
        return soup

    def remove_useless_attributes(self,soup):
        for tag in soup():
            for attribute in self.settings["useless_attributes"]:
                del tag[attribute]
        return soup

    def remove_white_spaces(self,soup):
        html = str(soup)
        html = "".join(line.strip() for line in html.split("\n"))
        soup = bs4.BeautifulSoup(html, "lxml")
        return soup

    def clear_useless_stuff(self,soup):
        # Remove all the comments
        if self.settings["clear_comments"] == True:
            soup = self.remove_comments_from_soup(soup)

        # Remove useless tag
        soup = self.remove_useless_tags(soup)

        # Remove useless attributes
        soup = self.remove_useless_attributes(soup)

        # Remove White Spaces
        soup = self.remove_white_spaces(soup)

        return soup

    #---------------------------------------------------------------------------

    def normalize_links(self,links):
        for i,link in enumerate(links):
            links[i] = uf.url_normalize(link,url)
        return links

    def add_link_to_urls(self,fahter,link):
            self.urls.add_node(father,link)

    def parse_links(self,soup,url):

        links = uf.get_links(soup)

        # construct relative urls
        links = self.normalize_links(links)

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
            html = uf.get_page(url,self.settings,self.logger)

            soup = bs4.BeautifulSoup(html, "lxml")

            # Clear the soup
            if self.settings["clear_html"] == True:
                soup = self.clear_useless_stuff(soup)

            # Update the cost of the node
            cost = self.cost_function(soup,link)
            self.urls.set_and_update_cost(link,cost)

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
            self.logger.error(e.message)

    def iteration(self):
        url = self.urls.get_next_page()

        if url == None:
            return False

        self.logger.info("current url: %s"%url)

        if self.settings["permessive_exception"]:
            self.permissive_check_and_parse(url)
        else:
            self.check_and_parse(urls)

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
                for i in range(num_of_iteration):
                    flag = self.iteration()
                    if flag == False:
                        break
            except KeyboardInterrupt:
                print("Stopping")



class WebList():
    index = 0
    urls = []

    def __init__(self,logger):
        self.logger = logger

    def add_node(self,father,link):
        self.urls.append(link)
        self.logger.info("Added Node %s"%link)

    def __len__(self):
        return len(self.urls)

    def __contains__(self,item):
        return item in self.urls

    def __str__(self):
        return str(self.urls)

    def get_next_page(self):
        if self.index < len(self.urls):
            url = self.urls[self.index]
            self.index += 1
            return url
        else:
            self.logger("There are no more nodes left")
            return None

    def set_and_update_cost(self,link,cost):
        return None
    def add_root(self,node):
        self.add_node("",node)