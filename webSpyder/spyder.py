
import webSpyder.helper_functions as hf
import webSpyder.helper_functions.urls_function as uf

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
    return str(type(f)) != "<class 'function'>"


class Spyder():

    settings = {
        "mode":"wget",
        "permessive_exception":True,
        "start_url":"",
        "project":"webSpyder",

        "clear_html":False,
        "clear_comments":True,
        "useless_tags":["svg","input","noscript","link","img","script","style"],
        "useless_attributes":["style", "href", "role", "src"],

        "cache":False,
        "cache_path":"%s/pagecaches/"%package_path[0],

        "log": True,
        "log_path":"%s/log/"%package_path[0].replace("\\\\","\\"),
        "log_format": '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    # Costructor
    #---------------------------------------------------------------------------

    def __init__(self,project=None):
        if project != None:
            self.settings["project"] = project

        self.filter_functions  = []
        self.functionList = []
        self.cost_function = self.default_cost_function
        start_url = self.settings["start_url"]

        # Setup the logger
        self.logger = logging.getLogger(self.settings["project"].replace(" ",""))
        self.file_handler = logging.FileHandler(self.settings["log_path"] + self.settings["project"] + '.log')
        self.formatter = logging.Formatter(self.settings["log_format"])
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.setLevel(logging.INFO)

        # Enable or disable the logger
        self.logger.disabled = not self.settings["log"]

        self.urls = linkGraph.linkGraph(self.logger)

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

    def set_start_url(self,value):
        self.settings["start_url"] = value
        self.urls = linkGraph.linkGraph(self.logger)
        self.urls.add_root(value)

    def set_cache_path(self,value):
        self.settings["cache_path"] = value

    def set_log_path(self,value):
        self.settings["log_path"] = value

    def set_log_format(self,value):
        self.settings["log_format"] = value



    # Main methods
    #---------------------------------------------------------------------------

    def default_cost_function(self,soup,link):
        return 1

    def _url_filer(self,url):
        for filter in self.filter_functions:
            result = filter(url)
            if result == False:
                return False

        return True

    def clear_useless_stuff(self,soup):
        # Remove all the comments
        if self.settings["clear_comments"] == True:
            comments = soup.findAll(text=lambda text:isinstance(text, bs4.Comment))
            for comment in comments:
                comment.extract()

        # Remove useless tag
        for tag in self.settings["useless_tags"]:
            for item in soup(tag):
                item.decompose()

        # Remove useless attributes
        for tag in soup():
            for attribute in self.settings["useless_attributes"]:
                del tag[attribute]

        html = str(soup)
        html = "".join(line.strip() for line in html.split("\n"))

        return bs4.BeautifulSoup(html, "lxml")

    def iteration(self):
        url = self.urls.get_next_page()

        if url == None:
            return False

        self.logger.info("current url: %s"%url)
        try:
            if self._url_filer(url):
                html = uf.get_page(url,self.settings,self.logger)

                soup = bs4.BeautifulSoup(html, "lxml")

                links = uf.get_links(soup)

                # construct relative urls
                for i,link in enumerate(links):
                    links[i] = uf.url_normalize(link,url)

                # add only valid urls that are not already in list and won't be filtered out
                for link in uf.links_not_in_urls(self.urls,links):
                    try:
                        #if a valid link and it has not to be filtered
                        if validators.url(link) and self._url_filer(link):
                            # if the link is new create the node
                            if link not in self.urls:
                                cost = self.cost_function(soup,link)
                                self.urls.add_node(link,cost)
                            # create the link between the page and the link
                            self.urls.add_edge(url,link)
                    #if everything goes bad the url is not valid
                    except ValidationFailure:
                        self.logger.warning("Found a non valid url %s"%link)

                # Clear the soup
                if self.settings["clear_html"] == True:
                    soup = self.clear_useless_stuff(soup)

                # Call the user functions
                for function in self.functionList:
                    function(soup,url)


        except Exception as e:
            self.logger.error("ERROR At the iteration over %s"%url)
            self.logger.error(e.message)
            # If the execution is not permessive, if there is an exception don't catch it
            if self.settings["permessive_exception"] == False:
                raise e
        return True

    def next(self):
            flag = self.iteration()
            if flag == False:
                raise StopIteration()

    def run(self):
        pbar = tqdm()

        flag = True
        try:
            while flag:
                flag = self.iteration()
                pbar.update(1)
        except KeyboardInterrupt:
            print("Stopping")

        pbar.close()

