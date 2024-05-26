from heapq import heappop, heappush
from itertools import permutations

from poo.map_poo import Graph
from poo.ships_poo import PassengersShips, CargoShips
from ships.ships import get_all_ships
from map.map import graphs, clear_screen
from pdf.pdf import create_pdf, create_pdf_passengers


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


# Function to find all the paths along two or more ports (used for passenger ships)
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


def route_passengers():
    try:
        start_port = input("Please, enter the starting port: ")

        if graphs[0].get_node(start_port) is None:
            print("The starting port does not exist.")
            return

        end_port = input("Please, enter the destination port: ")

        if graphs[0].get_node(end_port) is None:
            print("The destination port does not exist.")
            return

        forced_stops = input("Please enter the forced stops (separated by commas \",\"): ")

        forced_stops = [item.strip() for item in forced_stops.split(',') if item and not item.isspace()]

        current_forced_stops = set()

        for stop in forced_stops:
            if stop == start_port:
                print(f"The forced stop {stop} is the same as the start of the path")
                return

            if stop == end_port:
                print(f"The forced stop {stop} is the same as the end of the path")
                return

            if stop in current_forced_stops:
                print(f"The forced stop {stop} was introduced multiple times as a forced stop.")
                return

            current_forced_stops.add(stop)
            if graphs[0].get_node(stop) is None:
                print(f"The forced stop {stop} does not exist.")
                return

        max_days = int(input("Please enter the maximum number of days: "))

        paths, days = find_path_passengers(graphs[0], start_port, end_port, forced_stops, max_days)

        ships = get_all_ships()

        passenger_ships = [ship for ship in ships if isinstance(ship, PassengersShips)]

        clear_screen()
        for i in range(0, len(passenger_ships), 2):
            ship1 = f"{i + 1}. {passenger_ships[i].ship_name}"
            ship2 = f"{i + 2}. {passenger_ships[i + 1].ship_name}" if i + 1 < len(passenger_ships) else ""
            print(f"{ship1:<30} {ship2}")

        ship_choice = int(input("Please, choose a ship by entering its number: ")) - 1
        chosen_ship = passenger_ships[ship_choice]

        clear_screen()
        print(f"You have chosen the ship: {chosen_ship.ship_name}")

        if not paths:
            print(f"No path found in {max_days} days.")
            return

        if len(paths) != 1:
            print(f"{len(paths)} paths found:")
        else:
            print("1 path found:")

        for path, day in zip(paths, days):
            path_str = " -> ".join(path)
            print(f"Path: {path_str}, Days: {day}")

        response = input("Do you want to save this data in pdf (yes/no): ")

        if response.lower() == "yes":
            routes = list(zip(paths, days))
            create_pdf_passengers(start_port, end_port, chosen_ship.ship_name, routes, *forced_stops)
    except Exception as e:
        print(f"{e}")


# Function to find the shortest path between two ports and its budget (dijkstra style)
def find_shortest_path(map_: Graph, start_port: str, end_port: str):
    if start_port == end_port:  # In case the user decides to go to the same port
        return [start_port], 0, 0

    # Start the registry variables
    days_passed = {port: float('inf') for port in map_.nodes.keys()}
    path_budget = {port: None for port in map_.nodes.keys()}
    closest_port = {port: None for port in map_.nodes.keys()}
    visited_ports = set()

    days_passed[start_port] = 0

    # List that stores the ports to be searched
    search_list = [(0, 0, start_port)]

    while search_list:
        current_days, current_budget, current_port = heappop(search_list)

        if current_port in visited_ports:
            # In case the port was already visited, aka analyzed
            continue

        visited_ports.add(current_port)

        if current_port == end_port:
            break

        for neighbour_port, days_to_port in map_.get_node(current_port).connections.items():
            if days_to_port + current_days < days_passed[neighbour_port]:
                days_passed[neighbour_port] = days_to_port + current_days
                port_budget = map_.get_node(neighbour_port).value
                path_budget[neighbour_port] = current_budget + port_budget * days_to_port
                closest_port[neighbour_port] = current_port

                heappush(search_list, (days_passed[neighbour_port], path_budget[neighbour_port], neighbour_port))

    # In case the path isn't found
    if days_passed[end_port] == float('inf'):
        return None, None, None

    # Otherwise, build the path in a list
    finalPath = []
    finalPort = end_port

    while finalPort is not None:
        finalPath.insert(0, finalPort)
        finalPort = closest_port[finalPort]

    return finalPath, days_passed[end_port], path_budget[end_port]


# Function to find the shortest path along two or more ports and its budget (used for cargo ships)
def find_path_cargos(map_: Graph, start_port: str, end_port: str, forced_stops: list):
    if not forced_stops:
        # In case the user didn't insert any forced stop
        return find_shortest_path(map_, start_port, end_port)

    else:
        shortest_days = float('inf')

        for combination in permutations(forced_stops):
            combination_path = [start_port] + list(combination) + [end_port]
            test_days, test_budget = 0, 0
            test_path = []

            for i in range(len(combination_path) - 1):
                step_path, step_days, step_budget = find_shortest_path(map_, combination_path[i],
                                                                       combination_path[i + 1])

                if step_path is None:
                    # If, anywhere in the map, there are two ports unconnected
                    return None, None, None

                test_path += step_path
                test_days += step_days
                test_budget += step_budget

                if i != len(combination_path) - 2:
                    test_path.pop()  # Remove the last step, since it will be repeated

            # In case the path is shorter than the shortest previously found
            if test_days < shortest_days:
                shortest_days = test_days
                shortest_budget = test_budget
                shortest_path = test_path

        return shortest_path, shortest_days, shortest_budget


def route_cargos():
    try:
        start_port = input("Please enter the starting port: ")

        if graphs[1].get_node(start_port) is None:
            print("The starting port does not exist.")
            return

        end_port = input("Please enter the destination port: ")

        if graphs[1].get_node(end_port) is None:
            print("The destination port does not exist.")
            return

        forced_stops = input("Please enter the forced stops (separated by commas \",\"): ")

        forced_stops = [item.strip() for item in forced_stops.split(',') if item and not item.isspace()]

        current_forced_stops = set()

        for stop in forced_stops:
            if stop == start_port:
                print(f"The forced stop {stop} is the same as the start of the path")
                return

            if stop == end_port:
                print(f"The forced stop {stop} is the same as the end of the path")
                return

            if stop in current_forced_stops:
                print(f"The forced stop {stop} was introduced multiple times as a forced stop.")
                return

            current_forced_stops.add(stop)
            if graphs[1].get_node(stop) is None:
                print(f"The forced stop {stop} does not exist.")
                return

        max_days = int(input("Please enter the maximum number of days: "))

        path, days, budget = find_path_cargos(graphs[1], start_port, end_port, forced_stops)

        ships = get_all_ships()

        passenger_ships = [ship for ship in ships if isinstance(ship, CargoShips)]

        clear_screen()
        for i in range(0, len(passenger_ships), 2):
            ship1 = f"{i + 1}. {passenger_ships[i].ship_name}"
            ship2 = f"{i + 2}. {passenger_ships[i + 1].ship_name}" if i + 1 < len(passenger_ships) else ""
            print(f"{ship1:<30} {ship2}")

        ship_choice = int(input("Please, choose a ship by entering its number: ")) - 1
        chosen_ship = passenger_ships[ship_choice]

        clear_screen()
        print(f"You have chosen the ship: {chosen_ship.ship_name}")

        if not path:
            print("No path found.")
        else:
            path_str = " -> ".join(path)
            print(f"Shortest path found: {path_str}, Days: {days}, Cost: {budget}")

            if days > max_days:
                print(
                    f"WARNING!\nThis path takes {days - max_days} days more than the maximum amount of days inserted!")

            response = input("Do you want to save this data in pdf (yes/no): ")

            if response.lower() == "yes":
                routes = [(path, days)]
                create_pdf(start_port, end_port, chosen_ship.ship_name, routes, budget, f"{days} days", max_days,
                           *forced_stops)

    except Exception as e:
        print(f"{e}")
