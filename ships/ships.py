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
                ship_name=row["nome"],
                year_construction=row["anoConstrucao"],
                total_passengers=row["totalPassageiros"]
            )
        elif ship_class == CargoShips:
            ship = ship_class(
                ship_name=row["nome"],
                year_construction=row["anoConstrucao"],
                ship_class=row["classe"],
                ship_power=row["potência"]
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


pr = get_all_ships()

print(len(pr))
