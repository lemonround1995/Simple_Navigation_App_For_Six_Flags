"""
Team 3 

Aarushi Mishra (aarushi5)
Mengyuan Li (ml26)
Nan Yang (nanyang4)
Songwei Feng (songwei3)

This program is based on the map of Six Flags Magic Mountain. It generates navigation instructions for 21 attractions
that act as node for the generated graph. The graph consists of couple of nodes that have directed edges. This program
also informs about the alternative paths if the visitor is handicapped. Additionally, a visual presentation of graph
is generated as an output where each node is named and color-coded according to its attributes.

>Data files used: node.csv, edge.csv, edge_incomplete.csv
>Python files used: magic_map.py, MagicLA.py

Data File Description:
1. node.csv
> This csv file consists of 4 columns:
    1. id - attraction number as per the original map.
    2. name - name of the attraction
    3. type - type of attraction ( E / S / F)
    4. minimum_height - height of the attraction

2. edge.csv and edge_incomplete.csv
> This csv file consists of 5 columns:
    1. u_node - starting point of navigation
    2. v_node - end point of navigation
    3. weight - weight assigned to each edge ( Most of them calculated using Google maps, rest of them are assumed
    relatively.
    4. if_accessible - the value for this column is "Y" if the path is accessible for handicapped visitors,
    otherwise "N".
    5. if_directed - the value for this column is "Y" if the path is directed, otherwise "N".
Note: Difference between edge.csv and edge_incomplete.csv is that some edges have been removed in the later one to
validate the automated test.

"""
from MagicLA import MagicLA

print(" \n")
print("                     **** Welcome to Six Flags Magic Mountain, Los Angeles ****            \n")
print("                 >>>>>>  Get ready to enter the magical world of Magic Mountain <<<<<<    \n")
print("         From thrilling coasters to shopping and food, we’ve got them all listed here for you  \n")
print("Select your choice of attraction and get ready to ROCK and ROLL!!\n")
print("*Type : Entertainment (E), Store(S), Food Station(F) ")
print(" ")

# Create an instance of class MagicLA
magic_map = MagicLA("node.csv", "edge.csv")

# Iterate the graph, list the nodes information alphabetically
sorted_nodes_list = sorted(list(magic_map.nodes.items()), key=lambda data: data[1]['name'])
for node in sorted_nodes_list:
    print("Attraction ID: %s" % node[0])
    for attr_nm in node[1]:
        print("{}".format(attr_nm.title().replace("_", " ")) + ": %s" % node[1][attr_nm])
    print("=================================")

# Color the nodes according to their type (Entertainment/Store/Food Station)
magic_map.color_magic_map()

# Ask users to enter the query

print("Start Navigation!")
if_disabled = input("Are you the disabled?(Y/N): ")
source_temp = ""
while True:
    source = input("Please enter the ID of the start point(Press enter if you want to start from the last end point): ")
    if source == "" and source_temp == "":
        print("You must enter the start point! Try again!")
        continue

    target = input("Please enter the ID of the end point: ")
    if target == "":
        print("You must enter the end point! Try again!")
        continue

    if source == "" and source_temp != "":
        source = source_temp

    if if_disabled == "Y" or if_disabled == "y":
        magic_map.find_shortest_way_for_disabled(int(source), int(target))
    elif if_disabled == "N" or if_disabled == "n":
        magic_map.find_shortest_way(int(source), int(target))
    else:
        print("Invalid input! Try again!")

    source_temp = target
    ask_continue = input("Do you want to enter another navigation query?(Y/N): ")
    if ask_continue == "N" or ask_continue == "n":
        print("End navigation!")
        break
    elif ask_continue == "Y" or ask_continue == "y":
        continue
    else:
        print("Invalid input! Try again!")
        continue






