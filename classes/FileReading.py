from classes.CVRProblem import CVRProblem
from classes.Client import Client
from classes.Point import Point

def create_cvrp_problem(filepath="instances\instance.txt"):
    maximum_weight_load = 0
    depot_point = None
    clients_list = []
    with open(filepath, "r") as instance_file:
        for line in instance_file:
            if line == 'DEPOT_SECTION \n':
                depot_point = create_depot_point(instance_file)
                #print(depot_point)
    with open(filepath, "r") as instance_file:
        for line in instance_file:
            line_content = line.split(":")
            #print(line_content)
            if line_content[0] == "CAPACITY ":
                maximum_weight_load = int(line_content[1])
            elif line_content[0] == "NODE_COORD_SECTION \n":
                create_clients_from_node_coord_section(instance_file, clients_list)
    
    return CVRProblem(depot_point=depot_point, list_clients=clients_list, max_weight=maximum_weight_load)


def create_depot_point(file):
    depot_coordinates = []
    while len(depot_coordinates)<2:
        line = file.readline()
        depot_coordinates.append(float(line.replace("\n",'').replace(" ", "")))
    return Point(depot_coordinates[0], depot_coordinates[1])


def create_clients_from_node_coord_section(file, clients_list):
    demand_section = False
    while True:
        line = file.readline()
        if line.strip() == "DEPOT_SECTION":
            break
        
        if line.strip() == "DEMAND_SECTION":
            demand_section = True
            continue
        
        point_info = [info for index, info in enumerate(line.replace("\n",'').split(" "))]
        if not demand_section:
            clients_list.append(Client(float(point_info[2]),float(point_info[3])))
        else:
            clients_list[int(point_info[0])-1].set_packet_weight(float(point_info[1]))