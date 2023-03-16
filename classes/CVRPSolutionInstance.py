from typing import List
from classes.Route import Route


class CVRPSolutionInstance:
    def __init__(self, list_routes: List[Route]= []):
        self.list_routes = list_routes
        self.fitness = sum([route.fitness for route in list_routes])
