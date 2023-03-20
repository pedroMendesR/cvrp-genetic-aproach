from classes.CVRProblem import CVRProblem
from classes.Client import Client
from classes.Point import Point


def get_file_info(filepath="instances/instance.txt"):
    xlim = [0,0]
    ylim = [0,0]
    maximum_weight_load = 0
    depot_point = None
    clients_list = []
    with open(filepath, "r") as instance_file:
        for line in instance_file:
            line_content = line.split(":")
            #print(line_content)
            if "CAPACITY" in line_content[0]:
                maximum_weight_load = int(line_content[1])
            elif "NODE_COORD_SECTION" in line_content[0]:
                depot_point, xlim, ylim = create_clients_from_node_coord_section(instance_file, clients_list)
                #create_clients_from_node_coord_section(instance_file, clients_list)
    
    return {
        "xlim" : xlim,
        "ylim" : ylim,
        "maximum_weight_load" : maximum_weight_load,
        "depot_point" : depot_point,
        "clients_list" : clients_list
    }
    #return CVRProblem(depot_point=depot_point, list_clients=clients_list, max_weight=maximum_weight_load)


def create_depot_point(file):
    depot_coordinates = []
    while len(depot_coordinates)<2:
        line = file.readline()
        depot_coordinates.append(float(line.replace("\n",'').replace(" ", "")))
    return Point(depot_coordinates[0], depot_coordinates[1])


def create_clients_from_node_coord_section(file, clients_list):
    x_lim = [10000,-10000]
    y_lim = [10000,-10000]
    demand_section = False
    depot_point = None
    while True:
        line = file.readline()
        if line.strip() == "DEPOT_SECTION":
            break
        
        if line.strip() == "DEMAND_SECTION":
            demand_section = True
            continue
        
        point_info = [info for index, info in enumerate(line.replace("\n",'').split(" "))]
        #print(point_info)
        if not demand_section:
            x = float(point_info[1])
            y = float(point_info[2])
            x_lim[0] = x if x<x_lim[0] else x_lim[0]
            x_lim[1] = x if x>x_lim[1] else x_lim[1]
            y_lim[0] = y if y<y_lim[0] else y_lim[0]
            y_lim[1] = y if y>y_lim[1] else y_lim[1]
            if point_info[0] != '1':
                clients_list.append(Client(x,y))
                #print(clients_list[-1])
            else:
                depot_point = Point(float(point_info[1]),float(point_info[2]))
        elif point_info[0] != '1':
            clients_list[int(point_info[0])-2].set_packet_weight(float(point_info[1]))
    return depot_point, x_lim, y_lim