

import hashlib


class LinkTree:

    def __init__(self):
        self.linksTable = {}
        self.linksList = []

    def hasher(self,url):
        hasher = hashlib.md5()
        hasher.update(url.encode())
        return hasher.hexdigest()

    # Iterator
    def __iter__(self):
        self.iter_index = 0
        return self

    def next(self):
        if self.iter_index >= len(self.linksList):
            raise StopIteration()

        url_hash = self.linksList[self.iter_index]
        return self.linksTable[url_hash]["url"]

    # Helper stuff
    def __contains__(self,url):
        return self.hasher(url) in self.linksList

    def __len__(self):
        return len(self.linksList)

    def __getitem__(self,index):
        hash_url = self.linksList[index]
        return self.linksTable[hash_url]

    def __getattr__(self,url):
        hash_url = self.hasher(url)
        return self.linksTable[hash_url]

    def __str__(self):
        return str(self.linksTable)

    # Main Methods
    def add_link(self,link):
        # Get the url and the father url
        url = link.get_url()
        father = link.get_father()
        # Compute the hashes
        url_hash = self.hasher(url)
        father_hash = self.hasher(father)
        # Create the object
        link_node = {url_hash:link}
        # Add it to the hashtable
        self.linksTable.update(link_node)
        self.linksTable[father_hash].add_child(url)
        # Add the hash to the url list
        self.linkList.append(url_hash)

    def get_link(self,url):
        url_hash = self.hasher(url)
        return self.linksTable[url_hash]


class Link():

    def __init__(self,url,father,cost):
        self.url = url
        self.father = father
        self.cost = cost
        self.childs = []

    def __str__(self):
        node = {}
        node.update({"url":self.url})
        node.update({"cost":self.cost})
        node.update({"father":self.father_hash})
        node.update({"childs":self.childs})
        return str(node)

    def add_child(self,child_url):
        self.childs.append(child_url)
    
    def get_url(self):
        return self.url

    def get_father(self):
        return self.father

    def get_cost(self):
        return self.cost

    def get_childs(self):
        return self.childs