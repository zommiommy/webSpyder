import json

class linkGraph:
# Attributes -------------------------------------------------------------------
    # { start_link : [targets_link1,target_link2] }
    edge_dic = {}
    # { link : node }
    node_dic = {}
    # [link]
    node_without_chidrens = []

# Costructor -------------------------------------------------------------------
    def __init__(self,logger):
        """Initialize the linkGraph with the root link and use logger to log"""
        self.logger = logger
# Python methods overloads------------------------------------------------------
    def __contains__(self,item):
        return item in self.node_dic.keys()

    def __len__(self):
        return len(self.node_dic.keys())

    def __str__(self):
        result = "----------linkGraph----------\n"
        result += "node list: %s\n"%self.node_dic.keys()
        result += "edges: %s\n"%json.dumps(self.edge_dic, indent=4)
        return result

# Main methods------------------------------------------------------------------
    def add_root(self,root_link):
        self.edge_dic = {}
        self.node_dic = {}
        self.node_without_chidrens = []
        self.add_node(root_link,0)
    # O(1)
    def add_node(self,link,cost):
        """Create a node, add_node("www.google.com",root) will create a node with link www.google.com and father the root node """
        # add a node
        if link in self.node_dic.keys():
            self.logger.error("[Error] The node for %s already exist!"%link)
            return

        # create the node
        n = node(link)
        n.set_node_cost(cost)
        self.node_without_chidrens.append(link)
        self.node_dic.update({link:n})
        self.logger.info("Added the node  %s with cost %s"%(link,cost))

    # O(1) or O(num of node on the subtree with root end)
    def add_edge(self,start,end):
        """Add the edge to the graph add_edge(a,b) add an edge that goes a ---> b"""
        # if there is no start it's an error
        if start not in node_dic.keys():
            self.logger.error("[Error] There Is No start node %s"%start)
            return

        # if there is no end create it
        if end not in node_dic.keys():
            self.logger.error("[Error] There Is No end node %s"%end)
            return


        # update the cost of the path
        current_path_cost = self.node_dic[start].get_path_cost() + self.node_dic[end].get_node_cost()
        old_path_cost     = self.node_dic[end].get_path_cost()

        # if it has no father so no path add this.
        if  old_path_cost == node.INIFINTE_COST or  current_path_cost < old_path_cost:

            #if we added the node we need to delete the last link of the old path
            if current_path_cost < old_path_cost:
                father = self.node_dic[end].get_father()
                self.edge_dic[father].remove(end)
                self.logger.info("Deleted the edge from %s to %s"%(father,end))

            # update the end node
            self.node_dic[end].set_path_cost(current_path_cost)
            self.node_dic[end].set_father(start)
            self.logger.info("Updated the node %s"%(end))

            # Propagate the modification
            self.recalculate_cost(end)

            # if the node had no prevous edge create the edge
            if start in self.node_without_chidrens:
                self.edge_dic.update({start:[end]})
                self.node_without_chidrens.remove(start)
            # else just add the end to the list
            else:
                self.edge_dic[link].append(end)

            self.logger.info("Added the edge from %s to %s"%(start,end))
        # else if it's a worse path do nothing
        else:
            self.logger.info("Not Added the edge from %s to %s because it has path cost %s vs the current path cost %s"%(start,end,current_path_cost,old_path_cost))

    # warning O(num of unparsed nodes)
    # if max cost and min cost are similar then it's a width first search
    # the more the max cost is greater than the min cost the more it will work like a deept first search
    def get_next_page(self):
        """Find the unexplored leaf of the graph with min cost"""
        # max cost page
        node_list = self.node_dic.keys()
        nodes_with_childrens = self.edge_dic.keys()
        # Get unparsed leaf
        #  the fact that a node has children implies that it has been parsed except
        #  if it is a page with no links , Unprobabile but possible.
        leaf    = list(filter( lambda x: x if self.node_dic[x].is_parsed() else None,self.node_without_chidrens))

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
        tuples  = list(map(   lambda x  : (x,x.get_path_cost())))
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

    # warning O(num of node in the subtree with root start_node)
    def recalculate_cost(self,start_node):
        if start_node not in self.node_dic.keys():
            self.logger.error("[Error] The Start Node %s from which it have to recalculate the costs do not exist"%start_node)
            return

        if start_node not in self.edge_dic.keys():
            self.logger.info("The node %s has no childs so there is no need do go on reaclculating the costs"%start_node)
            return

        childs = self.edge_dic[start_node]
        start_path_cost = self.node_dic[start_node].get_path_cost()

        for child in childs:
            # Update the child path cost
            cost = self.node_dic[child].get_node_cost()
            self.node_dic[child].set_path_cost(start_path_cost + cost)

            # Propagate the modification
            self.recalculate_cost(child)

class node:
# Static Constant
    INIFINTE_COST = -1
    NO_FATHER = "No Father"

# Attributes -------------------------------------------------------------------
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

# Costructor -------------------------------------------------------------------
    def __init__(self,link):
        self.link = link

# Getter & Setter methods-------------------------------------------------------
    def get_link(self):
        return self.link


    def set_parsed(self):
        self.parsed = 1

    def get_parsed(self):
        return self.parsed

    def is_parsed(self):
        return self.parsed == 1


    def set_node_cost(self,new_cost):
        self.node_cost = new_cost

    def get_node_cost(self):
        return self.node_cost

    def set_path_cost(self,new_cost):
        self.path_cost = new_cost

    def get_path_cost(self):
        return self.path_cost


    def set_father(self,father):
        self.father = father

    def get_father(self):
        return self.father