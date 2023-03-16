import random
import matplotlib.pyplot as plt
import numpy as np
from classes.CVRPSolutionInstance import CVRPSolutionInstance
from classes.CVRProblem import CVRProblem
from classes.Client import Client

from classes.FileReading import get_file_info
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


test_routes_quantity = 2
test_routes = []
all_clients = []

info = get_file_info()

xlim_plot = [info['xlim'][0]*0.95, info['xlim'][1]*1.05]
ylim_plot = [info['ylim'][0]*0.95, info['ylim'][1]*1.05]


number_iterations = 1000
mutation_rate = 0.15
#cvrp.generate_first_route_population([(Route.generate_sweep_route, 1),(Route.generate_random_route,3)])

cvrp = CVRProblem(depot_point=info['depot_point'], list_clients=info['clients_list'], max_weight=info['maximum_weight_load'])
cvrp.generate_first_route_population([(Route.generate_sweep_route,150),(Route.generate_random_route,50)])

x_axis = [0]
y_axis = [CVRPSolutionInstance.get_better_route(cvrp.first_population)[1]]

print(x_axis)
print(y_axis)

last_generation = cvrp.first_population
last_generation_backup = last_generation

better_instance = None

for iteration in range(number_iterations):
    print(iteration)
    x_axis.append(iteration+1)
    offspring = []
    child_number = 0

    # CROSSOVER OPERATIONS
    while len(last_generation) > 1:
        parents = random.choices(last_generation, k=2)
        last_generation = [item for item in last_generation if item not in parents]
        #print(parents)
        offspring.append(CVRPSolutionInstance.exchange_position_crossover(parents[0],parents[1],cvrp.depot_point,cvrp.max_weight,range_max_weight_acceptable=[1,1]))

    # TOURNAMENTS OF PARENTS
    while len(last_generation_backup) > 1:
        parents = random.choices(last_generation_backup, k=2)
        last_generation_backup = [item for item in last_generation_backup if item not in parents]
        offspring.append(CVRPSolutionInstance.get_better_route(parents)[0])

    better_instance, value = CVRPSolutionInstance.get_better_route(offspring)

    y_axis.append(value)

    offspring.sort(key=lambda instance: instance.fitness)
    offspring = offspring[:200]

    # OFFSPRING MUTATION 

    for child in offspring:
        child.mutate_exchange(mutation_rate, cvrp.max_weight)



    last_generation = offspring
    last_generation_backup = offspring

#print(x_axis)
print(y_axis[-1])

fig, axs = plt.subplots(2)
axs[1].grid()
axs[1].plot(x_axis, y_axis)

instance_fit = 0

for index, route in enumerate(better_instance.list_routes):
    route.plot_route(axs[0], adjacent_matrix=cvrp.distances_adjacent_matrix, color=colors[index%len(colors)], depot_point=cvrp.depot_point)
    instance_fit += route.fitness

axs[0].set_xlim(xlim_plot)
axs[0].set_ylim(ylim_plot)
axs[0].plot(cvrp.depot_point.get_position_list()[0], cvrp.depot_point.get_position_list()[1], marker="o", color="b")
axs[0].grid()
print(f'Fitness Gráfico: {instance_fit}')
plt.show()

#new = CVRPSolutionInstance.exchange_position_crossover(random.choice(cvrp.first_population), random.choice(cvrp.first_population), cvrp.depot_point, cvrp.max_weight)
'''


fig = plt.figure()
axs = fig.subplots(2)

index_instances = 0

instance_fit = 0
for index, route in enumerate(cvrp.first_population[index_instances].list_routes):
    route.plot_route(axs[0], adjacent_matrix=cvrp.distances_adjacent_matrix, color=colors[index%len(colors)], depot_point=cvrp.depot_point)
    instance_fit += route.fitness

axs[0].set_xlim(xlim_plot)
axs[0].set_ylim(ylim_plot)
axs[0].plot(cvrp.depot_point.get_position_list()[0], cvrp.depot_point.get_position_list()[1], marker="o", color="b")
axs[0].grid()
print(f'Fitness Gráfico {index_instances+1} : {instance_fit}')

plt.show()

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

CVRPSolutionInstance.exchange_position_crossover(random.choice(cvrp.first_population), random.choice(cvrp.first_population))

plt.show()
'''