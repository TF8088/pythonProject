from heapq import heappop, heappush
from itertools import permutations

from poo.map_poo import Graph
# from ships.ships import get_all_ships
from map.map import graphs


# Function to find all the paths between two ports
def find_all_paths(map_: Graph, current_port: str, end_port: str, max_days: int, path=None, current_days=0,
                   all_paths=None, all_days=None):
    # The currentPort is the same as the startPort in the first call of the function

    if path is None:
        path = []
        all_paths = []
        all_days = []

    # Flags the current port as 'visited' by adding it to the path
    path.append(current_port)

    # In case we have arrived to our destination in the number of days allocated
    if current_port == end_port and current_days <= max_days:
        all_paths.append(path.copy())
        all_days.append(current_days)

    # In case we passed the number of days allocated or have arrived our destination
    if current_days > max_days or current_port == end_port:
        path.pop()
        return

    # Explore all the neighbour ports of the current port
    for neighbourPort, days in map_.get_node(current_port).connections.items():
        if neighbourPort not in path:
            find_all_paths(map_, neighbourPort, end_port, max_days, path, current_days + days, all_paths, all_days)

    path.pop()

    return all_paths, all_days


# Function to find all the paths along two or more ports (used for passengers)
def find_path_passengers(map_: Graph, start_port: str, end_port: str, forced_stops: list, max_days: int):
    # Function to organize the paths form shortest to longest
    def sort_paths(paths_, days_):
        for i_ in range(len(paths_) - 1):
            for j in range(i_ + 1, len(paths_)):
                if days_[i_] > days_[j]:
                    days_[i_], days_[j] = days_[j], days_[i_]
                    paths_[i_], paths_[j] = paths_[j], paths_[i_]

        return paths_, days_

    if not forced_stops:
        paths, days = find_all_paths(map_, start_port, end_port, max_days)
        return sort_paths(paths, days)  # Sort the paths before returning them

    else:
        allPaths, allDays = [], []

        for combination in permutations(forced_stops):
            combinationPath = [start_port] + list(combination) + [end_port]

            searchList = [(0, [])]

            for i in range(len(combinationPath) - 1):
                futureSearchList = []

                while searchList:
                    currentDays, currentPath = heappop(searchList)

                    partialPaths, partialDays = find_all_paths(map_, combinationPath[i], combinationPath[i + 1],
                                                               max_days - currentDays)

                    for stepPath, stepDays in zip(partialPaths, partialDays):
                        if i != len(combinationPath) - 2:
                            stepPath.pop()

                        heappush(futureSearchList, (currentDays + stepDays, currentPath + stepPath))

                searchList = futureSearchList

            while searchList:
                finalDays, finalPaths = heappop(searchList)

                allDays.append(finalDays)
                allPaths.append(finalPaths.copy())

        return sort_paths(allPaths, allDays)


def route_finder(i):
    startPort = input("Por favor, insira o porto de partida: ")

    if graphs[i].get_node(startPort) is None:
        print("The starting port deos not exist.")
        return

    endPort = input("Por favor, insira o porto de destino: ")

    if graphs[i].get_node(startPort) is None:
        print("The destination port deos not exist.")
        return

    forcedStops = input("Please enter the forced stops (separated by commas \",\"): ")

    forcedStops = [item.strip() for item in forcedStops.split(',') if item and not item.isspace()]

    for stop in forcedStops:
        if graphs[0].get_node(stop) is None:
            print(f"The forced stop {stop} does not exist.")
            return

    maxDays = int(input("Please enter the maximum number of days: "))

    paths, days = find_path_passengers(graphs[0], startPort, endPort, forcedStops, maxDays)

    if not paths:
        print("No path found.")
        return

    print("Path finded:")
    for path, day in zip(paths, days):
        print(f"Path: {path}, Days: {day}")
