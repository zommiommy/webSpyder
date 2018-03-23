

class DataInterface():

    def __init__(self,logger):
        self.logger = logger

    def add_node(self,father,link):
        raise Exception("add_node not implemented!")

    def __len__(self):
        raise Exception("__len__ not implemented!")

    def __contains__(self,item):
        raise Exception("__contains__ not implemented!")

    def __str__(self):
        raise Exception("__str__ not implemented!")

    def get_next_page(self):
        raise Exception("get_next_page not implemented!")

    def set_and_update_cost(self,link,cost):
        raise Exception("set_and_update_cost not implemented!")

    def add_root(self,node):
        raise Exception("add_root not implemented!")
