import matplotlib.pyplot as plt
import numpy as np

from classes.FileReading import create_cvrp_problem
from classes.Route import Route

#CONFIGS
depot_coordinates = [1,1]
xlim_client = [-30,30]
ylim_client = [-30,30]
packet_weight_lim = [1,6]
number_clients = 4

xlim_plot = [-2,100]
ylim_plot = [-2,100]
colors = [['r','#EC6969'],['g', '#69EC69'],['black', '#aaaaaa'],['purple', '#D790FF']]

show_point_id_subtitle = False
show_point_weight_subtitle = False

test_routes_quantity = 2
test_routes = []
all_clients = []


cvrp = create_cvrp_problem()

#print(cvrp.__str__())
# print(np.matrix(cvrp.distances_adjacent_matrix).shape)
# for clients in cvrp.list_clients:
#     print(clients)

cvrp.generate_first_route_population([(Route.generate_sweep_route, 1),(Route.generate_random_route,3)])

fig = plt.figure()
axs = fig.subplots(2,2)

index_instances = 0

for i in range(2):
    for j in range(2):
        instance_fit = 0
        for index, route in enumerate(cvrp.first_population[index_instances].list_routes):
            route.plot_route(axs[i,j], adjacent_matrix=cvrp.distances_adjacent_matrix, color=colors[index%len(colors)], depot_point=cvrp.depot_point)
            instance_fit += route.fitness

        axs[i,j].set_xlim(xlim_plot)
        axs[i,j].set_ylim(ylim_plot)
        axs[i,j].plot(cvrp.depot_point.get_position_list()[0], cvrp.depot_point.get_position_list()[1], marker="o", color="b")
        axs[i,j].grid()
        print(f'Fitness Gráfico {index_instances+1} : {instance_fit}')
        index_instances += 1


plt.show()