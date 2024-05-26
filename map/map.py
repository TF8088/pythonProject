import networkx as nx
import matplotlib.pyplot as plt
import os

from poo.map_poo import Graph, Node

graphPassengers = Graph({
    "Algeciras": {"connections": {"Le Havre": 6, "Valencia": 2, "Botas": 8}},
    "Valencia": {"connections": {"Algeciras": 2}},
    "Marseille": {"connections": {"Amsterdam": 6, "Hamburg": 8, "Izmit": 8, "Le Havre": 4}},
    "Le Havre": {"connections": {"Algeciras": 6, "Marseille": 4, "Antwerp": 2}},
    "Antwerp": {"connections": {"Le Havre": 2}},
    "Amsterdam": {"connections": {"Hamburg": 1, "Marseille": 6}},
    "Hamburg": {"connections": {"Amsterdam": 1, "Izmit": 10, "Marseille": 8}},
    "Botas": {"connections": {"Izmit": 4, "Algeciras": 8}},
    "Izmit": {"connections": {"Botas": 4, "Marseille": 8, "Hamburg": 10}}
})

graphCargos = Graph({
    "Algeciras": {"connections": {"Le Havre": 5, "Valencia": 1}, "value": 83493},
    "Valencia": {"connections": {"Algeciras": 1, "Marseille": 3}, "value": 60116},
    "Marseille": {"connections": {"Le Havre": 3, "Izmit": 9, "Botas": 12, "Amsterdam": 5, "Valencia": 3},
                  "value": 75617},
    "Le Havre": {"connections": {"Marseille": 3, "Algeciras": 5, "Antwerp": 1}, "value": 66104},
    "Antwerp": {"connections": {"Le Havre": 1}, "value": 201202},
    "Amsterdam": {"connections": {"Marseille": 5}, "value": 98517},
    "Botas": {"connections": {"Izmit": 4, "Marseille": 12}, "value": 70917},
    "Izmit": {"connections": {"Botas": 4, "Marseille": 9}, "value": 72690}
})

graphs = [graphPassengers, graphCargos]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def see_ports(i):
    try:
        G = nx.Graph()

        for port in graphs[i].nodes.values():
            port_label = f"{port.name} ({port.value})" if port.value is not None else port.name
            G.add_node(port_label)

            for connection, distance in port.connections.items():
                connection_label = f"{connection} ({graphs[i].get_node(connection).value})" if (
                        graphs[i].get_node(connection).value is
                        not None) else connection
                G.add_edge(port_label, connection_label, weight=distance)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        plt.show()
    except Exception as e:
        print(f"{e}")


def see_port(i):
    try:
        portName = str(input("Insert the name of the port: ")).strip()

        port = graphs[i].get_node(portName)

        if port is None:
            print("Port not Found. ")
            return

        clear_screen()
        print(f"Name: {port.name}")
        print("Connections: ")

        for connection, distance in port.connections.items():
            print(f"\t - {connection} : {distance}")

        if i == 1 and port.value is not None:
            print(f"Value: {port.value} $")
    except Exception as e:
        print(f"{e}")


def create_port(i):
    try:
        portName = str(input("Insert the name of the port: ")).strip()

        if not portName:
            return

        if graphs[i].get_node(portName) is not None:
            print(f"The port {portName} already exists.")
            return

        connections = {}

        while True:
            connection_name = str(input(f"Enter the name of a connection to {portName}"
                                        " (or 'exit' to terminate): ")).strip()

            if connection_name.lower() == 'exit':
                break

            if graphs[i].get_node(connection_name) is None:
                print(f"The {connection_name} port does not exist. Please try again. ")
                continue

            connection_distance = int(input(f"Enter the distance for the connection {connection_name}: "))

            if connection_distance > 0:
                connections[connection_name] = connection_distance

        value = None
        if i == 1:
            value = int(input("Enter the value for the port: "))

            if value <= 0:
                print(f"The budget set to {portName} cannot be lower or equal to 0")
                return

        # Add itself to the map
        new_node = Node(portName, connections, value)

        # Add the connections of the other ports to itself
        graphs[i].add_node(new_node)
    except Exception as e:
        print(f"{e}")


def edit_port(i):
    try:
        portName = str(input("Enter the name of the port to edit: ")).strip()

        port = graphs[i].get_node(portName)

        if port is None:
            print(f"The port {portName} does not exist.")
            return

        value = None

        while True:
            print("\n╔═══════════════════════════════════════╗")
            print("║              Edit Options:            ║")
            print("╠═══════════════════════════════════════╣")
            print(f"\t1. Port Name: {portName}")
            print(f"\t2. Connections: {port.connections}")
            if i == 1:
                print(f"\t3. Value: {port.value}")
            print("\t0. Exit")
            print("╚═══════════════════════════════════════╝")
            if i == 1:
                option = input("Enter the number of the field (0-3): ").strip()
            else:
                option = input("Enter the number of the field (0-2): ").strip()

            if option == '1':
                new_name = input("Enter the new name: ")

                if not new_name:
                    clear_screen()
                    continue

                if graphs[i].get_node(new_name) is None:
                    graphs[i].update_node_name(portName, new_name)
                    portName = new_name

                else:
                    clear_screen()
                    print(f"{new_name} already exists!")
                    continue

            elif option == '2':
                connection_name = str(input("Enter the name of a connection (or 'exit' to finish): ")).strip()

                if connection_name.lower() == 'exit':
                    break

                if graphs[i].get_node(connection_name) is None:
                    clear_screen()
                    print(f"The port {connection_name} does not exist. Please try again.")
                    continue

                connection_distance = int(input(f"Enter the distance to the connection {connection_name}: "))

                if connection_distance > 0:
                    port.connections[connection_name] = connection_distance

                else:
                    graphs[i].remove_connection(portName, connection_name)

            elif option == '3' and i == 1:
                value = int(input("Enter the value for the port: "))

                if value < 0:
                    value = port.value

            elif option == '0':
                break
            else:
                clear_screen()
                print("Invalid option. Please try again.")
                continue

            graphs[i].update_node(portName, port.connections, value)
            clear_screen()
    except Exception as e:
        print(f"{e}")


def delete_port(i):
    try:
        portName = str(input("Insert the name of the port to edit: ")).strip()

        port = graphs[i].get_node(portName)

        if port is None:
            print(f"The port {portName} does not exist.")
            return

        print(f"Name: {port.name}")
        print("Connections: ")

        for connection, distance in port.connections.items():
            print(f"\t - {connection} : {distance}")

        confirm = str(input("Are you sure you want to delete this port? (yes/no): ")).strip()

        if confirm.lower() == "yes":
            graphs[i].delete_node(portName)
            print(f"Port {portName} has been deleted. ")
        else:
            print("Deletion Cancelled.")

    except Exception as e:
        print(f"{e}")
