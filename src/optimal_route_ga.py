import os
from itertools import combinations
import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
import folium
import googlemaps
from IPython.display import display


class OptimalRoute:

    def __init__(self, waypoint_combinations_distance_df=None,
                 waypoints_lst=None, api_key=None,
                 mode='driving', language='English',
                 units='metric', verbose=True):
        '''
            :param waypoint_combinations_distance_df: pandas data frame containing the following columns: waypoint1, waypoitn2, distance_m, duration_s
            :type waypoint_combinations_distance_df: pandas df

            :param waypoints_lst: list containing all the destinations that need to be visited
            :type waypoints_lst: list

            :param api_key: google developer api key
            :type api_key: string

            :param mode: google parameter for mean of travel
            :type mode: string

            :param language: google parameter for language
            :type language: string

            :param units: google parameter for units
            :type units: string

            :param verbose: print progressing scores and best population every 10th generation
            :type verbose: boolean



        '''
        self.waypoint_distances = {}
        self.waypoint_durations = {}
        self.verbose = verbose
        self.api_key = api_key
        self.optimal_route_lat_lst = []
        self.optimal_route_lon_lst = []

        if waypoints_lst:
            self.waypoints_lst = waypoints_lst
            gmaps = googlemaps.Client(key=api_key)

            for (waypoint1, waypoint2) in combinations(waypoints_lst, 2):
                try:
                    route = gmaps.distance_matrix(origins=[waypoint1],
                                                  destinations=[waypoint2],
                                                  mode=mode,
                                                  language=language,
                                                  units=units)

                    # "distance" is in meters
                    distance = route["rows"][0]["elements"][0]["distance"]["value"]

                    # "duration" is in seconds
                    duration = route["rows"][0]["elements"][0]["duration"]["value"]

                    self.waypoint_distances[frozenset([waypoint1, waypoint2])] = distance
                    self.waypoint_durations[frozenset([waypoint1, waypoint2])] = duration

                except Exception as e:
                    print("Error with finding the route between %s and %s." % (waypoint1, waypoint2))
        else:
            waypoints_lst = []
            for i, row in waypoint_combinations_distance_df.iterrows():
                self.waypoint_distances[frozenset([row.waypoint1, row.waypoint2])] = row.distance_m
                self.waypoint_durations[frozenset([row.waypoint1, row.waypoint2])] = row.duration_s
                self.waypoints_lst.append(row.waypoint1)
                self.waypoints_lst.append(row.waypoint2)
            self.waypoints_lst = list(set(waypoints_lst))

    def compute_fitness(self, solution):

        """
            This function returns the total distance traveled on the current road trip.

            The genetic algorithm will favor road trips that have shorter
            total distances traveled.

            :param solution: list of tuples as candidate solution
            :type solution: list

        """
        self.solution_fitness = 0.0
        
        for index in range(len(solution)):
            waypoint1 = solution[index - 1]
            waypoint2 = solution[index]
            self.solution_fitness += self.waypoint_distances[frozenset([waypoint1, waypoint2])]

        return self.solution_fitness

    def generate_random_agent(self):
        """
            Generates a random road trip from the waypoints.
        """

        new_random_agent = self.waypoints_lst
        random.shuffle(new_random_agent)
        return tuple(new_random_agent)

    def mutate_agent(self, agent_genome, max_mutations=3):
        """
            Applies `max_mutations` - 1 point mutations to the given road trip.

            A point mutation swaps the order of two waypoints in the road trip.

            :param agent_genome: cantidate solution
            :type agent_genome:

            :param max_mutations: number of mutations to be applied on the agent_genome
            :type max_mutations: int
        """

        agent_genome = list(agent_genome)
        num_mutations = random.randint(1, max_mutations)

        for mutation in range(num_mutations):
            swap_index1 = random.randint(0, len(agent_genome) - 1)
            swap_index2 = swap_index1

            while swap_index1 == swap_index2:
                swap_index2 = random.randint(0, len(agent_genome) - 1)

            agent_genome[swap_index1], agent_genome[swap_index2] = agent_genome[swap_index2], agent_genome[swap_index1]

        return tuple(agent_genome)

    def shuffle_mutation(self, agent_genome):
        """
            Applies a single shuffle mutation to the given road trip.

            A shuffle mutation takes a random sub-section of the road trip
            and moves it to another location in the road trip.
        """

        agent_genome = list(agent_genome)

        start_index = random.randint(0, len(agent_genome) - 1)
        length = random.randint(2, 20)

        genome_subset = agent_genome[start_index:start_index + length]
        agent_genome = agent_genome[:start_index] + agent_genome[start_index + length:]

        insert_index = random.randint(0, len(agent_genome) + len(genome_subset) - 1)
        agent_genome = agent_genome[:insert_index] + genome_subset + agent_genome[insert_index:]

        return tuple(agent_genome)

    def generate_random_population(self, pop_size):
        """
            Generates a list with `pop_size` number of random road trips.
        """
        random_population = []
        for agent in range(pop_size):
            random_population.append(self.generate_random_agent())
        return random_population

    def run_genetic_algorithm(self, generations=5000, population_size=100):
        """
            The core of the Genetic Algorithm.

            `generations` and `population_size` must be a multiple of 10.
        """
        population_subset_size = int(population_size / 10.)
        generations_10pct = int(generations / 10.)

        # Create a random population of `population_size` number of solutions.
        population = self.generate_random_population(population_size)

        # For `generations` number of repetitions...
        for generation in range(generations):

            # Compute the fitness of the entire current population
            population_fitness = {}

            for agent_genome in population:
                if agent_genome in population_fitness:
                    continue

                population_fitness[agent_genome] = self.compute_fitness(agent_genome)

            # Take the top 10% shortest road trips and produce offspring each from them
            new_population = []
            for rank, agent_genome in enumerate(sorted(population_fitness,
                                                       key=population_fitness.get)[:population_subset_size]):
                if self.verbose:
                    if (generation % generations_10pct == 0 or generation == generations - 1) and rank == 0:
                        print("Generation %d best: %d | Unique genomes: %d" % (generation,
                                                                               population_fitness[agent_genome],
                                                                               len(population_fitness)))
                        print(agent_genome)
                        print("")

                # Create 1 exact copy of each of the top road trips
                new_population.append(agent_genome)

                # Create 2 offspring with 1-3 point mutations
                for offspring in range(2):
                    new_population.append(self.mutate_agent(agent_genome, 3))

                # Create 7 offspring with a single shuffle mutation
                for offspring in range(7):
                    new_population.append(self.shuffle_mutation(agent_genome))

            # Replace the old population with the new population of offspring
            for i in range(len(population))[::-1]:
                del population[i]

            population = new_population
            self.optimal_route = sorted(population_fitness, key=population_fitness.get)[0]
        return self.optimal_route

    def write_data_tsv(self, file_name):
        '''
            Write data for
        '''
        with open("{}.tsv".format(file_name), "w") as out_file:
            out_file.write("\t".join(["waypoint1",
                                      "waypoint2",
                                      "distance_m",
                                      "duration_s"]))

            for (waypoint1, waypoint2) in self.waypoint_distances.keys():
                out_file.write("\n" +
                               "\t".join([waypoint1,
                                          waypoint2,
                                          str(self.waypoint_distances[frozenset([waypoint1, waypoint2])]),
                                          str(self.waypoint_durations[frozenset([waypoint1, waypoint2])])]))

    def find_location_centre(self, lat_lst, lon_lst):
        return [sum(lat_lst) / len(lat_lst), sum(lon_lst) / len(lon_lst)]

    def origin_dest_pair(self, route_lst):
        return list(zip(route_lst, route_lst[1:])) + [(route_lst[1:][-1], route_lst[0])]

    def draw_optimal_route_map(self, zoom_start=13, file_path_name=None):
        gmaps = googlemaps.Client(key=self.api_key)
        for destination in self.optimal_route:
            resp = gmaps.geocode(destination)
            self.optimal_route_lon_lst.append(resp[0]['geometry']['location']['lng'])
            self.optimal_route_lat_lst.append(resp[0]['geometry']['location']['lat'])
        self.optimal_route_centre = self.find_location_centre(self.optimal_route_lat_lst, self.optimal_route_lon_lst)
        self.optimal_route_map = folium.Map(location=self.optimal_route_centre, tiles='cartodbpositron',
                                       zoom_start=zoom_start)
        for location in zip(self.optimal_route, self.optimal_route_lon_lst, self.optimal_route_lat_lst):
            folium.Marker([location[2],
                           location[1]],
                          popup=location[0],
                          icon=folium.Icon(color='blue')).add_to(self.optimal_route_map)
        for location in zip(self.optimal_route, self.optimal_route_lon_lst, self.optimal_route_lat_lst):
            folium.Marker([location[2],
                           location[1]],
                          popup=location[0],
                          icon=folium.Icon(color='blue')).add_to(self.optimal_route_map)

        for coors in self.origin_dest_pair(list(zip(self.optimal_route_lat_lst, self.optimal_route_lon_lst))):
            origin_lat = coors[0][0]
            origin_lon = coors[0][1]
            destination_lat = coors[1][0]
            destination_lon = coors[1][1]
            folium.PolyLine([[origin_lat, origin_lon],
                             [destination_lat, destination_lon]]).add_to(self.optimal_route_map)

        if file_path_name:
            self.optimal_route_map.save(file_path_name)

    def display_optimal_route_map(self):
        display(self.optimal_route_map)