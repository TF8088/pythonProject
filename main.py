from route.router import route_passengers, route_cargos
from map.map import create_port, see_port, see_ports, edit_port, delete_port
from poo.menu_poo import Menu, Submenu


def main():
    menu = Menu("Nautilus Logistics", "Select an option:")

    route_menu = Submenu("Path Finder", "Choose an option:")
    route_menu.add_option("See routes for passenger ships", route_passengers)
    route_menu.add_option("See the shortest route for cargo ships", route_cargos)

    passengers_menu = Submenu("Passenger Ports Management", "Choose an option:")
    passengers_menu.add_option("View Ports (UI)", see_ports, 0)
    passengers_menu.add_option("View Port", see_port, 0)
    passengers_menu.add_option("Create Port", create_port, 0)
    passengers_menu.add_option("Edit Port", edit_port, 0)
    passengers_menu.add_option("Delete Port", delete_port, 0)

    cargo_menu = Submenu("Cargo Ports Management", "Choose an option:")
    cargo_menu.add_option("View Ports (UI)", see_ports, 1)
    cargo_menu.add_option("View Port", see_port, 1)
    cargo_menu.add_option("Create Port", create_port, 1)
    cargo_menu.add_option("Edit Port", edit_port, 1)
    cargo_menu.add_option("Delete Port", delete_port, 1)

    menu.add_submenu("Path Finder", route_menu)
    menu.add_submenu("Passenger Ports Management", passengers_menu)
    menu.add_submenu("Cargo Ports Management", cargo_menu)
    menu.show()


if __name__ == '__main__':
    main()
