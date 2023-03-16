import math
import random
from typing import List
from classes.Client import Client

from classes.Point import Point


class Route:

    def __init__(self, client_path: List[Point], max_load_supported: float = 10):
        self.client_path = client_path
        self.cost = Route.get_route_cost(client_path, Point.get_euclidian_distance)
        self.fitness = self.cost if Route.get_route_integrity(client_path, max_load_supported) else float('inf')

    def __str__(self):
        route = ''
        for index, client in enumerate(self.client_path):
            route = route + client.__str__(index=index) + '\n'
        return f'A rota com custo {self.cost} possui o caminho:\n{route}'

    def plot_route(self, axes_plot, adjacent_matrix: List[List[float]]=[], color:List[str]=['r','#EC6969'], depot_point:Point = Point(0,0)):
        #print(self.client_path)
        for index, client in enumerate(self.client_path):
            client0, client1 = self.client_path[index], self.client_path[(index+1)%len(self.client_path)]
            client0_position, client1_position = client0.get_position_list(), client1.get_position_list()
            x_axis = [client0_position[0], client1_position[0]]
            y_axis = [client0_position[1], client1_position[1]]
            
            axes_plot.plot(x_axis, y_axis, '--' if index == 0 or index == len(self.client_path)-1 else '-', color=color[1])
            

            #print(f'[{client0.id}][{client1.id}]')
            axes_plot.text((x_axis[0]+x_axis[1])/2, (y_axis[0]+y_axis[1])/2, str(adjacent_matrix[client0.id][client1.id])) if adjacent_matrix != [] \
            else axes_plot.text((x_axis[0]+x_axis[1])/2, (y_axis[0]+y_axis[1])/2, str(index))

            if client.x_position != depot_point.get_position_list()[0] and client.y_position != depot_point.get_position_list()[1]:
                client.plot_client(axes_plot, color[0], index)
    
    @staticmethod
    def get_route_integrity(route_client_path: List[Point], max_load_supported: float = 10):
        sum_weights = sum(client.packet_weight for client in route_client_path if type(client) == Client)
        return True if sum_weights <= max_load_supported else False

    @staticmethod
    def get_route_cost(route_client_path: List[Point], distance_function_applied: callable = Point.get_euclidian_distance) -> float:
        total_route_cost = 0
        for index in range(len(route_client_path)):
            parcial_route = distance_function_applied(route_client_path[index], route_client_path[(index+1)%len(route_client_path)])
            total_route_cost = total_route_cost + parcial_route
        return total_route_cost
        
    @staticmethod
    def generate_random_route(list_clients: List[Client], depot_point) -> List[Client]:
        random_list = list_clients[:]
        random.shuffle(random_list)
        return random_list

    @staticmethod
    def sweep_function(client: Client, depot_point: Point):
        result = 0
        y_difference = client.y_position-depot_point.y_position
        x_difference = client.x_position-depot_point.x_position
        if y_difference >= 0 and x_difference > 0:
            result = math.atan((y_difference)/(x_difference))
        elif y_difference > 0 and x_difference == 0:
            result = math.pi/2
        elif x_difference < 0:
            result = math.pi + math.atan((y_difference)/(x_difference))
        elif y_difference < 0 and x_difference == 0:
            result = 3*(math.pi/2)
        elif y_difference < 0 and x_difference > 0:
            result = 2*math.pi + math.atan((y_difference)/(x_difference))
        else:
            print(x_difference)
            print(y_difference)
            print(client)
            print(depot_point)
            input()
        return result

    @staticmethod
    def generate_sweep_route(list_clients: List[Client], depot_point: Point) -> List[Client]:
        sweep_list = list_clients[:]
        sweep_list.sort(key=lambda client : Route.sweep_function(client, depot_point))
        return sweep_list
    