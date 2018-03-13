import json

class linkGraph:
        # Attributes -------------------------------------------------------------------
            # { "node_link" : {"node":,node,parsed_childs":[node,node],"unparsed_childs":[node,node\] } }
    node_dic = {}


# Costructor -------------------------------------------------------------------
    def __init__(self,logger):
        """Initialize the linkGraph with the root link and use logger to log"""
        self.logger = logger
# Python methods overloads------------------------------------------------------
    def __contains__(self,item):
        return

    def __len__(self):
        return

    def __str__(self):
        return

# DT Interface methods----------------------------------------------------------
    def add_root(self, root_link):
        return

    def find_node(self,link):
        return

    def add_node(self,url,link):
        return

    def get_node_childs(self,link):
        return

    def get_unparsed_node(self):
        return

    def list_of_nodes(self):
        return self.node_dic.keys()

# Main methods------------------------------------------------------------------
    def update_node(self,father,link,cost,childs_list):
        c = self.node_dic[link]
        c["node"].set_node_cost(cost)

        for child in childs_list:
            self.add_node(link,child)



    def predict_cost(self,link):
        return
    def choose_random(self,cost_list):
        return

    def get_next_page(self):
        return













class node:
    # Static Constant
    INIFINTE_COST = -1
    NO_FATHER = ""

# Attributes -----------------------------------------------------------------
    # the link (STRING)
    link = ""
    # 0 if not parsed 1 if already parsed (0 or 1)
    parsed = 0
    # the cost of the node, (MINIMIZATION PROBLEM) (INT)
    node_cost = INIFINTE_COST
    # the cost of the path to that node (INT)
    path_cost = INIFINTE_COST
    # the father of the node (STRING)
    father = NO_FATHER

# Costructor -----------------------------------------------------------------
    def __init__(self, link):
        self.link = link

# Getter & Setter methods-----------------------------------------------------
    def get_link(self):
        return self.link

    def set_parsed(self):
        self.parsed = 1

    def get_parsed(self):
        return self.parsed

    def is_parsed(self):
        return self.parsed == 1

    def set_node_cost(self, new_cost):
        self.node_cost = new_cost

    def get_node_cost(self):
        return self.node_cost

    def set_path_cost(self, new_cost):
        self.path_cost = new_cost

    def get_path_cost(self):
        return self.path_cost

    def set_father(self, father):
        self.father = father

    def get_father(self):
        return self.father
