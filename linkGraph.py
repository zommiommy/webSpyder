

class linkGraph:
# Attributes -------------------------------------------------------------------
    # { start_link : [targets_link1,target_link2] }
    edge_list = {}
    # { link : node }
    node_dic = {}

# Costructor -------------------------------------------------------------------
    def __init__(self,root_link,logger):
        """Initialize the linkGraph with the root link and use logger to log"""
        self.add_node(root_link,0)
        self.logger = logger

# Python methods overloads------------------------------------------------------
    def __contains__(self,item):
        return item in self.node_dic.keys()

    def __len__(self):
        return len(self.node_dic.keys())

# Main methods------------------------------------------------------------------

    def add_edge(self,start,end):
        """Add the edge to the graph add_edge(a,b) add an edge that goes a ---> b"""
        # if there is no start it's an error
        if start not in node_dic.keys():
            self.logger.error("[Error] There Is No start node %s"%start)
            return

        # if there is no end create it
        if start not in node_dic.keys():
            self.logger.error("[Error] There Is No end node %s"%end)
            return

        # if the node had no prevous edge create the edge
        if start not in self.edge_list.keys():
            self.edge_list.update({start:[end]})
        # else just add the end to the list
        else:
            self.edge_list[link].append(end)
        # add the edge to the edge_list
        self.logger.info("Added the edge from %s to %s"%(start,end))

    def add_node(self,link,cost):
        """Create a node, add_node("www.google.com") will create a node with link www.google.com """
        # add a node
        if link in self.node_dic.keys():
            self.logger.error("[Error] The node for %s already exist!"%link)
            return
        # create the node
        n = node(link)
        n.set_node_cost(cost)
        self.node_dic.update({link:n})
        self.logger.info("Added the node  %s with cost %s"%(link,cost))

    def get_next_page():
        """Find the unexplored leaf of the graph with min cost"""
        # max cost page
        node_list = self.node_dic.keys()
        nodes_with_childrens = self.edge_list.keys()
        # Get unparsed leaf
        #  the fact that a node has children implies that it has been parsed except
        #  if it is a page with no links , Unprobabile but possible.
        leaf    = list(filter(lambda x  : x if x not in nodes_with_childrens and x.is_parsed() else None,node_list))

        # if there are no node you can't go on searching
        if len(leaf) == 0:
            self.logger.error("[Error] There are no more page left to parse")
            return
        # if there is only one node use it.
        if len(leaf) == 1:
            leaf[0].set_parsed()
            return leaf[0].get_link()
        # if there are at least two node search for the best

        # Get Leaf into tuples of node and cost to get easy compares
        tuples  = list(map(   lambda x  : (x,x.cost)))
        # Find the minimum
        minimum  = list(reduce(lambda x,y: x if x[1] <= y[1] else y,tuples))
        min_node = minimum[0]
        min_cost = minimum[1]
        min_link = min_node.get_link()
        self.logger.info("The best node is %s with cost %s"%(min_link,min_cost))
        # Set the node as parsed
        min_node.set_parsed()
        # Return the max utility url
        return min_link



class node:
# Attributes -------------------------------------------------------------------
    # the link
    link = ""
    # 0 if not parsed 1 if already parsed
    parsed = 0
    # the cost of the node, (MINIMIZATION PROBLEM)
    cost = -1

# Costructor -------------------------------------------------------------------
    def __init__(self,link):
        self.link = link

# Getter & Setter methods-------------------------------------------------------
    def get_link(self):
        return self.link

    def set_node_cost(self,new_cost):
        self.cost = new_cost

    def get_node_cost(self):
        return self.cost

    def set_parsed(self):
        self.parsed = 1

    def get_parsed(self):
        return self.parsed

    def is_parsed(self):
        return self.parsed == 1