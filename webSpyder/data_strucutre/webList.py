

from webSpyder.data_strucutre.data_interface import DataInterface

class WebList(DataInterface):
    index = 0
    urls = []

    def __init__(self,logger,settings):
        self.logger = logger
        self.settings = settings

    def add_node(self,father,link):
        self.urls.append(link)
        #self.logger.info("Added Node %s"%link)

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
            self.logger.info("There are no more nodes left")
            return None

    def set_and_update_cost(self,link,cost):
        return None

    def add_root(self,node):
        self.add_node("",node)
