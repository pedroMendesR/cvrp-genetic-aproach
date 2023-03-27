import os
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


test_routes = []
all_clients = []

info = get_file_info()

xlim_plot = [info['xlim'][0]*0.95, info['xlim'][1]*1.05]
ylim_plot = [info['ylim'][0]*0.95, info['ylim'][1]*1.05]


population_size = 200
constructed_population = 0.05
number_iterations = 200

mutation_rate = 0.1
crossover_rate = 0.9

crossover_function = CVRPSolutionInstance.modified_crossover # exchange_position_crossover
mutation_function = CVRPSolutionInstance.scramble_mutation    #    mutate_exchange

trials_number = 10
result_vector = []

x_axis = []
y_axis = []
#,run2,run3,run4,run5,run6,run7,run8,run9,run10
first_file=True
arr = os.listdir('..\instances\A')
#input(arr)
with open(f'..\data_modified_crossover_scramble_mutation.csv','w') as file:
    if first_file:
        file.write('instance,run1,run2,run3,run4,run5,run6,run7,run8,run9,run10\n')
        first_file = False

    for name_file in arr:

        info = get_file_info(f'..\instances\A\{name_file}')
        #input(info)
        #xlim_plot = [info['xlim'][0]*0.95, info['xlim'][1]*1.05]
        #ylim_plot = [info['ylim'][0]*0.95, info['ylim'][1]*1.05]

        file.write(f'{info["name"]}')
        for trial in range(trials_number):

            initial_population = [int(constructed_population*population_size),population_size-int(constructed_population*population_size)]

            cvrp = CVRProblem(depot_point=info['depot_point'], list_clients=info['clients_list'], max_weight=info['maximum_weight_load'])
            cvrp.generate_first_route_population([(Route.generate_sweep_route,initial_population[0]),(Route.generate_random_route,initial_population[1])])

            x_axis = [0]
            y_axis = [CVRPSolutionInstance.get_better_route(cvrp.first_population)[1]]

            #print(x_axis)
            #print(y_axis)

            last_generation = cvrp.first_population

            better_instance = None

            for iteration in range(number_iterations):
                print(name_file, '.', trial,'.',iteration)
                x_axis.append(iteration+1)
                offspring = []
                child_number = 0
                parents_list = []
                for instance in last_generation:
                    list_routes_temp = []
                    for route in instance.list_routes:
                        clients_temp = route.client_path[:]
                        list_routes_temp.append(Route(clients_temp, cvrp.max_weight))
                    parents_list.append(CVRPSolutionInstance(list_routes_temp))
                # CROSSOVER OPERATIONS
                crossover_probability = random.uniform(0,1)
                #
                for i in range(sum(initial_population)):
                    parents = random.choices(last_generation, k=2)
                    #print('cross: ', i)
                    #last_generation = [item for item in last_generation if item not in parents]
                    if crossover_probability < crossover_rate:
                        #offspring.append(CVRPSolutionInstance.exchange_position_crossover(parents[0],parents[1],cvrp.depot_point,cvrp.max_weight,range_max_weight_acceptable=[1,1]))
                        #offspring.append(random.choice(parents))
                        #offspring.append(CVRPSolutionInstance.modified_crossover(parents[0],parents[1],cvrp.depot_point,cvrp.max_weight))
                        offspring.append(crossover_function(parents[0],parents[1],cvrp.depot_point,cvrp.max_weight))
                        #input(offsprings_crossover)
                    else:
                        offspring.append(parents[0])
                        offspring.append(parents[1])

                # OFFSPRING MUTATION 
                #print([child.fitness for child in parents_list])
                #input(len(parents_list))
                for child in offspring:
                    child.mutate_exchange(mutation_rate, cvrp.max_weight)
                #input(len(parents_list))
                #input([child.fitness for child in parents_list])



                #print(type(offspring[0]))
                #print(type(parents_list[0]))

                offspring_backup = offspring + parents_list
                #input(len(offspring_backup))
                offspring = []
                

                # TOURNAMENTS OF OFFSPRING
                i = 0
                while len(offspring_backup) > 1:
                    #print(i)
                    i += 1
                    parents_index = random.sample([index for index in range(len(offspring_backup))], 2)
                    parents = [offspring_backup[parents_index[0]], offspring_backup[parents_index[1]]]

                    offspring_backup = [item for index,item in enumerate(offspring_backup) if index not in parents_index]
                    offspring.append(parents[0] if parents[0].fitness < parents[1].fitness else parents[1])
                    #offspring.append(CVRPSolutionInstance.get_better_route(parents)[0])

                #input(len(offspring_backup))
                if len(offspring_backup) == 1:
                    offspring.append(offspring_backup[0])
                    
                offspring.sort(key=lambda instance: instance.fitness)
                #print([child.fitness for child in offspring])
                
                offspring = offspring[:population_size]
                #input([child.fitness for child in offspring])

                better_instance, value = CVRPSolutionInstance.get_better_route(offspring)

                

                y_axis.append(value)

            

                

                last_generation = offspring

            file.write(f',{y_axis[-1]}')
            result_vector.append(y_axis[-1])

        file.write('\n')
    file.close()

# for index,result in enumerate(result_vector):
#     print(index,' : ', result)
# print('mean value: ', sum(result_vector,0.0)/trials_number)

#print(y_axis[-1])

# fig, axs = plt.subplots(2)
# axs[1].grid()
# axs[1].plot(x_axis, y_axis)

# instance_fit = 0

# for index, route in enumerate(better_instance.list_routes):
#     route.plot_route(axs[0], adjacent_matrix=cvrp.distances_adjacent_matrix, color=colors[index%len(colors)], depot_point=cvrp.depot_point)
#     instance_fit += route.fitness

# axs[0].set_xlim(xlim_plot)
# axs[0].set_ylim(ylim_plot)
# axs[0].plot(cvrp.depot_point.get_position_list()[0], cvrp.depot_point.get_position_list()[1], marker="o", color="b")
# axs[0].grid()
# #print(f'Fitness Gráfico: {instance_fit}')
# plt.axhline(y = int(info['optimal']), color = 'r', linestyle = '-')
# plt.show()

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