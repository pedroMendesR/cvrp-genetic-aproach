import random
from typing import List, Tuple
from classes.CVRPSolutionInstance import CVRPSolutionInstance
from classes.Client import Client
from classes.Point import Point
from classes.Route import Route


class CVRProblem:

    def __init__(self, depot_point: Point = Point(0,0), list_clients: List[Client]= [], read_clients_from_file: bool = False, \
                 instance_file="instance.txt", number_clients: int=10, xlim: List[float] = [-10,10], \
                    ylim: List[float]= [-10,10], packet_weight_lim: List[float] = [1,6], max_weight: float = 10):
        self.list_clients = list_clients if list_clients != [] \
            else CVRProblem.read_clients_from_file(instance_file) \
                if read_clients_from_file else CVRProblem.generate_random_clients(number_clients, xlim, ylim, packet_weight_lim)
        self.depot_point = depot_point
        self.distances_adjacent_matrix = CVRProblem.generate_distances_adjacent_matrix(self.list_clients, self.depot_point)
        self.max_weight = max_weight
        self.first_population = []

    def __str__(self):
        cvrp_string = f'\n===========================\nDepot Point: {self.depot_point.__str__()}\nMax weight: {self.max_weight}'
        return cvrp_string
    
    def generate_first_route_population(self, instances_by_method: List[Tuple[callable,int]] = [(Route.generate_random_route,9)]):

        instances_created = []

        for method, quantity in instances_by_method:
            for _ in range(quantity):

                population_order_list = method(self.list_clients, self.depot_point)
                routes_list = []
                temp_list = []
                for index, client_ordered in enumerate(population_order_list):
                    if sum([client.packet_weight for client in temp_list]) + client_ordered.packet_weight <= self.max_weight:
                        temp_list.append(client_ordered)
                        if index != len(population_order_list)-1:
                            continue
                    temp_list.insert(0, self.depot_point)
                    routes_list.append(Route(temp_list,self.max_weight))
                    last_route = index == len(population_order_list)-1 and client_ordered not in temp_list
                    temp_list = [client_ordered]
                    if last_route:
                        temp_list.insert(0, self.depot_point)
                        routes_list.append(Route(temp_list,self.max_weight))

                instances_created.append(CVRPSolutionInstance(routes_list))
        self.first_population = instances_created



    @staticmethod
    def generate_distances_adjacent_matrix(list_clients, depot_point):
        distance_matrix = []
        all_points = list_clients[:]
        all_points.insert(0,depot_point)

        for root in all_points:
            distance_list = [round(Point.get_euclidian_distance(root, client_goal),2) for client_goal in all_points]
            distance_matrix.append(distance_list)
        return distance_matrix

    @staticmethod
    def generate_random_clients(number_clients: int = 10, xlim: List[float] = [-10,10], ylim: List[float]= [-10,10], packet_weight_lim: List[float] = [1,6]):
        list_clients = [Client(round(random.uniform(xlim[0],xlim[1]), 2), round(random.uniform(ylim[0],ylim[1]),2), random.randint(packet_weight_lim[0],packet_weight_lim[1])) for _ in range(number_clients)]
        return list_clients
    
    