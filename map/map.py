from poo.map_poo import Graph, Node

graphPassengers = Graph({
    "Algeciras": {"connections": {"Le Havre": 6, "Valencia": 2, "Botas": 8}},
    "Valencia": {"connections": {"Algeciras": 2}},
    "Marseille": {"connections": {"Amsterdam": 6, "Hamburg": 8, "Izmit": 8, "Le Havre": 4}},
    "Le Havre": {"connections": {"Algeciras": 6, "Marseille": 4, "Antwerp": 2}},
    "Antwerp": {"connections": {"Le Havre": 2}},
    "Amsterdam": {"connections": {"Hamburg": 1, "Marseille": 6}},
    "Hamburg": {"connections": {"Amsterdam": 1, "Izmit": 10, "Marseille": 8}},
    "Botas": {"connections": {"Izmit": 4, "Valencia": 8}},
    "Izmit": {"connections": {"Botas": 4, "Marseille": 8, "Hamburg": 10}}
})

graphCargos = Graph({
    "Algeciras": {"connections": {"Le Havre": 5, "Valencia": 1}, "value": 83493},
    "Valencia": {"connections": {"Algeciras": 1, "Marseille": 3}, "value": 60116},
    "Marseille": {"connections": {"Le Havre": 3, "Izmit": 9, "Botas": 12, "Amsterdam": 5}, "value": 75617},
    "Le Havre": {"connections": {"Marseille": 3, "Algeciras": 5}, "value": 66104},
    "Antwerp": {"connections": {"Le Havre": 1}, "value": 201202},
    "Amsterdam": {"connections": {"Marseille": 5}, "value": 98517},
    # "Hamburg": {"connections": {"Amsterdam": 1, "Izmit": 10, "Marseille": 8}, "value": 118761},
    "Botas": {"connections": {"Izmit": 4, "Marseille": 12}, "value": 70917},
    "Izmit": {"connections": {"Botas": 4, "Marseille": 9}, "value": 72690}
})

graphs = [graphPassengers, graphCargos]


# TODO Implementar UI
def see_port(i):
    try:
        portName = str(input("Insert the name of the port: ")).strip()

        port = graphs[i].get_node(portName)

        if port is None:
            print("Port not Found. ")
            return

        print(f"Name: {port.name}")
        print("Connections: ")

        for connection, distance in port.connections.items():
            print(f"\t - {connection} : {distance}")

        if i == 1 and port.value is not None:
            print(f"Value: {port.value} $")

        input("Press Enter to continue...")
    except Exception as e:
        print(f"{e}")


def create_port(i):
    try:
        portName = str(input("Insert the name of the port: ")).strip()

        if graphs[i].get_node(portName) is not None:
            print(f"The port {portName} already exists.")
            return

        connections = {}

        while True:
            connection_name = str(input("Enter the name of a connection to this"
                                        " port (or 'exit' to terminate): ")).strip()

            if connection_name.lower() == 'exit':
                break

            if graphs[i].get_node(connection_name) is None:
                print(f"The {connection_name} port does not exist. Please try again. ")
                continue

            connection_distance = int(input(f"Enter the distance for the connection {connection_name}: "))

            connections[connection_name] = connection_distance

        value = None
        if i == 1:
            value = int(input("Enter the value for the port: "))

        new_node = Node(portName, connections, value)

        graphs[i].add_node(new_node)
    except Exception as e:
        print(f"{e}")


def edit_port(i):
    try:
        portName = str(input("Insert the name of the port to edit: ")).strip()

        port = graphs[i].get_node(portName)

        if port is None:
            print(f"The port {portName} does not exist.")
            return

        print("Enter the new connections for this port (or 'exit' to terminate)")

        connections = {}

        while True:
            connection_name = str(input("Enter the name of a connection (or 'exit' to terminate): ")).strip()

            if connection_name.lower() == 'exit':
                break

            if graphs[i].get_node(connection_name) is None:
                print(f"The {connection_name} port does not exist. Please try again. ")
                continue

            connection_distance = int(input(f"Enter the distance for the connection {connection_name}: "))

            connections[connection_name] = connection_distance

            if i == 1:
                value = int(input("Enter the value for the port: "))
            else:
                value = None

            graphs[i].update_node(portName, connections, value)
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
