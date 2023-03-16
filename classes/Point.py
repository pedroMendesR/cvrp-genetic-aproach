from math import sqrt


class Point:

    counter = -2

    def __init__(self, x_position: float, y_position: float):
        self.x_position = x_position
        self.y_position = y_position
        self.id = Point.counter
        Point.counter = Point.counter + 1

    def __str__(self, index=-1):
        return f'[{index}]  ({self.x_position}, {self.y_position}) com id {self.id}'
    
    def get_position_list(self):
        return [self.x_position, self.y_position]

    @staticmethod
    def get_euclidian_distance(client_1: 'Point', client_2: 'Point') -> float:
        return sqrt(pow(client_2.x_position - client_1.x_position, 2) +pow(client_2.y_position - client_1.y_position, 2))
        
    @staticmethod
    def get_mah_distance(client_1: 'Point', client_2: 'Point') -> float:
        return abs(client_2.x_position - client_1.x_position) +abs(client_2.y_position - client_1.y_position)