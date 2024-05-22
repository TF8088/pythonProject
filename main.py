from route.router import route_freighters, route_passengers
from map.map import create_port, see_port, edit_port, delete_port
from poo.menu import Menu, Submenu


def main():
    # 2.1 - Ver Mapa (Ver Grafo / interfaçe grafica)
    # Opcao de selecionar barco

    menu = Menu("Nautilus Logistics", "Select an option:")

    route_menu = Submenu("Route Builder", "Choose an option:")
    route_menu.add_option("See shortest route for Freighters", route_freighters)
    route_menu.add_option("See routes for Passengers", route_passengers)

    passengers_menu = Submenu("Passenger Management", "Choose an option:")
    passengers_menu.add_option("View Port", see_port, 0)
    passengers_menu.add_option("Create Port", create_port, 0)
    passengers_menu.add_option("Edit Port", edit_port, 0)
    passengers_menu.add_option("Delete Port", delete_port, 0)

    cargo_menu = Submenu("Freighters Management", "Choose an option:")
    cargo_menu.add_option("View Port", see_port, 1)
    cargo_menu.add_option("Create Port", create_port, 1)
    cargo_menu.add_option("Edit Port", edit_port, 1)
    cargo_menu.add_option("Delete Port", delete_port, 1)

    menu.add_submenu("Passenger Management", passengers_menu)
    menu.add_submenu("Cargo Management", cargo_menu)

    menu.show()


if __name__ == '__main__':
    main()
