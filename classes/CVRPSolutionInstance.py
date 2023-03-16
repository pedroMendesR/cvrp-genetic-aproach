import random
from typing import List
from classes.Client import Client
from classes.Point import Point
from classes.Route import Route


class CVRPSolutionInstance:
    def __init__(self, list_routes: List[Route]= []):
        self.list_routes = list_routes
        self.fitness = sum([route.fitness for route in list_routes])

    def mutate_exchange(self, mutation_rate, max_load):
        if random.uniform(0,1) < mutation_rate:
            index = random.randint(0,len(self.list_routes)-1)
            clients_path = self.list_routes[index].client_path

            index0 = random.randint(1,len(clients_path)-1)
            index1 = random.randint(1,len(clients_path)-1)
            
            aux = clients_path[index0]
            clients_path[index0] = clients_path[index1]
            clients_path[index1] = aux

            self.list_routes[index] = Route(clients_path, max_load)
            self.update_list_routes(self.list_routes)
            
    def update_list_routes(self, list_routes: List[Route]):
        self.list_routes = list_routes
        self.fitness = sum([route.fitness for route in list_routes])

    @staticmethod
    def exchange_position_crossover(parent0: 'CVRPSolutionInstance', parent1: 'CVRPSolutionInstance', depot_point: Point, max_weight: float, range_max_weight_acceptable: List[float]=[1,1]):
        #print(parent0.list_routes)
        #print(parent1.list_routes)
        (parent_index, parent_routes) = (parent0,parent1) if random.randint(0,1) == 0 else (parent1,parent0)
        route_index = random.choice(parent_index.list_routes).client_path[1:]
        route_copied = random.choice(parent_routes.list_routes).client_path[1:]

        indexes = [client.id-1 for client in route_index][:1]

        child_clients_sort = sum(list(map(lambda route: route.client_path, parent_index.list_routes)),[])
        child_clients_sort = [client for client in child_clients_sort if type(client) == Client and client not in route_copied]

        index = 0
        for client in route_copied:
            if indexes[index] >= len(child_clients_sort):
                child_clients_sort.insert(-1, client)
            else:
                child_clients_sort.insert(indexes[index], client)
            index = (index+1)%len(indexes)

        routes = CVRPSolutionInstance.split_list_to_routes(child_clients_sort, depot_point, max_weight, range_max_weight_acceptable)
        #input(routes)
        return CVRPSolutionInstance(routes)

    @staticmethod
    def split_list_to_routes(list_clients: List[Client], depot_point: Point, max_weight: float, range_max_weight_acceptable: List[float]=[1,1]):
        list_clients_routes = []
        
        
        temp_route = [depot_point]
        temp_max_weight = max_weight*random.uniform(range_max_weight_acceptable[0], range_max_weight_acceptable[1])
        #print(temp_max_weight)
        #index = 0
        for index, client in enumerate(list_clients):
            last_added = False
            if sum([client_temp.packet_weight for client_temp in temp_route[1:]]) + client.packet_weight <= temp_max_weight:
                temp_route.append(client)
                last_added = True
                if index != len(list_clients)-1:
                    continue
            list_clients_routes.append(Route(temp_route,max_weight))
            temp_route = [depot_point,client]
            temp_max_weight = max_weight*random.uniform(range_max_weight_acceptable[0], range_max_weight_acceptable[1])

            if index == len(list_clients)-1 and not last_added:
                list_clients_routes.append(Route(temp_route,max_weight))

        clients_returned = [route.client_path for route in list_clients_routes]
        clients_returned = [client for client in sum(clients_returned,[]) if type(client) == Client]
        
        return list_clients_routes
    
    @staticmethod
    def get_better_route(solution_instances: List['CVRPSolutionInstance']):
        temp_route = solution_instances[0]
        temp_route_value = solution_instances[0].fitness
        for solution in solution_instances[1:]:
            if solution.fitness < temp_route_value:
                temp_route_value = solution.fitness
                temp_route = solution
        return [temp_route, temp_route_value]