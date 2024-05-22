import os
import pandas as pd
from poo.ships_poo import PassengersShips, CargoShips

file_path = os.path.join(os.path.dirname(__file__), '..', 'navios_mercantes.xlsx')

xls = pd.ExcelFile(file_path)


def read_ship_data(sheet_name, ship_class):
    df = pd.read_excel(xls, sheet_name=sheet_name)
    ships = []

    for i, row in df.iterrows():
        ship = None
        if ship_class == PassengersShips:
            ship = ship_class(
                shipName=row["nome"],
                yearConstruction=row["anoConstrucao"],
                totalPassengers=row["totalPassageiros"]
            )
        elif ship_class == CargoShips:
            ship = ship_class(
                shipName=row["nome"],
                yearConstruction=row["anoConstrucao"],
                shipClass=row["classe"],
                shipPower=row["potência"]
            )
        ships.append(ship)

    return ships


def get_all_ships():
    ship_type_map = {
        'navios_passageiros': PassengersShips,
        'navios_de_carga': CargoShips,
    }

    all_ships = []

    for sheet_name, ship_class in ship_type_map.items():
        ships = read_ship_data(sheet_name, ship_class)
        all_ships.extend(ships)

    return all_ships
