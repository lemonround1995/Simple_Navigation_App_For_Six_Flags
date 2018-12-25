import networkx as nx
import csv
import matplotlib.pyplot as plt


class MagicLA(nx.DiGraph):
    """ This class is extended from class DiGraph. Each instance of this class is a directed
    graph where each node represents an attraction.

    """
    # Set the names of nodes attributes and edges attributes as private class variables
    __key_for_node_attrs = "id"
    __node_attrs = ["id", "name", "type"]
    __key_for_edge_attrs = ("u_node", "v_node")
    __edge_attrs = ["u_node", "v_node", "if_accessible", "if_directed", "weight"]

    def __init__(self, node_file, edge_file):     # init method added
        nx.DiGraph.__init__(self)

        # Create the node attributes dict and edge attributes dict
        node_attrs_dict = self.load_nodes_data(node_file)
        edge_attrs_dict = self.load_edges_data(edge_file)

        # Add nodes, nodes attributes, edges, edges attributes to the graph
        self.add_nodes_and_attributes(node_attrs_dict)
        self.add_edges_and_attributes(edge_attrs_dict)

    def load_nodes_data(self, file_name) -> dict:
        """Given the file_name of nodes data in csv format, load the data and covert it to a dict.
           The key of the dict is node id.
           The value of the dict is also a dict whose keys are nodes attributes and values are
           relevant attribute data like name, type and minimum height.

           :param file_name: file name of nodes data
           :return: a node attribute dict as described above
        """
        with open(file_name, "r") as data_file:
            node_data = csv.DictReader(data_file)
            node_data_list = [dict(row) for row in node_data]

        node_attrs_dict = {}
        for node_data in node_data_list:
            attrs_key = int(node_data[MagicLA.__key_for_node_attrs])
            node_data.pop(MagicLA.__key_for_node_attrs)
            node_attrs_dict[attrs_key] = node_data

        self.node_attrs_dict = node_attrs_dict

        return node_attrs_dict

    def load_edges_data(self, file_name) -> dict:
        """Given the file_name of edges data in csv format, load the data and covert it to a dict.
           The key of the dict is edge id, the format is (u_node, v_node)
           The value of the dict is also a dict whose keys are edges attributes and values are
           relevant attribute data like weight, directed or not and accessible or not.

           :param file_name: file name of edges data
           :return: a edge attribute dict as described above
        """
        with open(file_name, "r") as data_file:
            edge_data = csv.DictReader(data_file)
            edge_data_list = [dict(row) for row in edge_data]

        edge_attrs_dict = {}
        for edge_data in edge_data_list:
            attrs_key = (int(edge_data[MagicLA.__key_for_edge_attrs[0]]), int(edge_data[MagicLA.__key_for_edge_attrs[1]]))
            attrs_key_mirror = (int(edge_data[MagicLA.__key_for_edge_attrs[1]]), int(edge_data[MagicLA.__key_for_edge_attrs[0]]))
            edge_data[MagicLA.__edge_attrs[4]] = int(edge_data[MagicLA.__edge_attrs[4]])
            edge_data.pop(MagicLA.__key_for_edge_attrs[0])
            edge_data.pop(MagicLA.__key_for_edge_attrs[1])

            # if the edge is a double-way, then both (u_node, v_node) and (v_node, u_node) should be added as keys
            if edge_data[MagicLA.__edge_attrs[3]] == "N":
                edge_attrs_dict[attrs_key] = edge_data
                edge_attrs_dict[attrs_key_mirror] = edge_data

            # if the edge is a single-way, then only need to add (u_node, v_node)
            else:
                edge_attrs_dict[attrs_key] = edge_data

        self.edge_attrs_dict = edge_attrs_dict

        return edge_attrs_dict

    def add_nodes_and_attributes(self, node_attrs_dict):
        """Given the node attributes dict as described above, add the nodes and their
        attributes to the graph.

           :param node_attrs_dict
        """
        node_list = [key for key in node_attrs_dict]
        self.add_nodes_from(node_list)
        nx.set_node_attributes(self, node_attrs_dict)

    def add_edges_and_attributes(self, edge_attrs_dict):
        """Given the edge attributes dict as described above, add the edges and their
        attributes to the graph.

           :param edge_attrs_dict
        """
        edge_list = [key for key in edge_attrs_dict]
        self.add_edges_from(edge_list)
        nx.set_edge_attributes(self, edge_attrs_dict)

    def find_shortest_way(self, source, target):
        """Given the source node and target node, find the shortest path.
        Print out the shortest distance and turn-by-turn navigation.
        This method does not apply to disabled people.

           :param source: the start point, should be the node ID
           :param target: the end point, should be the node ID

         """
        result_tuple = nx.single_source_dijkstra(self, source, target, weight="weight")
        path_tuple_list = []
        i = 0
        while i <= len(result_tuple[1]) - 2:
            path_tuple_list.append((result_tuple[1][i], result_tuple[1][i + 1]))
            i += 1

        # if the shortest distance is larger than 999, then at least one path is not accessible
        if result_tuple[0] < 100000:
            print("The shortest distance from %s to %s is %s feet" % (source, target, result_tuple[0]))
            print("The path should be: ")
            for path_tuple in path_tuple_list:
                print("%s(%s) ----> %s(%s)" % (
                path_tuple[0], self.node_attrs_dict[path_tuple[0]][MagicLA.__node_attrs[1]], \
                path_tuple[1], self.node_attrs_dict[path_tuple[1]][MagicLA.__node_attrs[1]],))
        else:
            print("Sorry, there is no path from %s(%s) to %s(%s) for you." % (
            source, self.node_attrs_dict[source][MagicLA.__node_attrs[1]],
            target, self.node_attrs_dict[target][MagicLA.__node_attrs[1]]))

    def find_shortest_way_for_disabled(self, source, target):
        """Given the source node and target node, find the shortest path.
           Print out the shortest distance and turn-by-turn navigation.
           This method only applies to disabled people

           :param source: the start point, should be the node ID
           :param target: the end point, should be the node ID
         """
        # if a path is not accessible, set its weight value to 999
        for key, value in self.edges.items():
            if value[MagicLA.__edge_attrs[2]] == "N":
                value[MagicLA.__edge_attrs[4]] = 100000
        self.find_shortest_way(source, target)

    def verify_all_paths(self) -> bool:         # included for doctest
        """ This method checks if there exists a path between one node and every other node
        in the graph.
        This method has two automated doctest.The second test is a negative test to check
        if the method works as expected when one or more directed edges is removed from the graph.

        :param : self
        :return: boolean

        >>> a = MagicLA("node.csv", "edge.csv")
        >>> print(a.verify_all_paths())
        True
        >>> b = MagicLA("node.csv", "edge_incomplete.csv")
        >>> print(b.verify_all_paths())
        False
        """
        path = True
        nodes_1 = self.nodes
        for n in self.nodes:
            for i in nodes_1:
                if nx.has_path(self, n, i):
                    pass
                else:
                    return False
        return path

    def color_magic_map(self):
        """ This method colors the node of the graph generated according to the type of attraction. According to
        this color code, the attractions of entertainment (E) type are colored red,the attractions of
        shop(S) type are colored green and the attractions of Food Station (F) type are colored yellow.

        """
        node_color_list = []
        for key, value in self.nodes.items():  # changed from dict to networkx
            if value["type"] == "E":
                node_color_list.append("r")
            if value["type"] == "S":
                node_color_list.append("g")
            if value["type"] == "F":
                node_color_list.append("y")

        plt.axis("off")
        nx.draw_networkx(self, node_color=node_color_list)

        plt.show()
