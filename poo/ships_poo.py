class Ship:
    def __init__(self, ship_name, year_construction):
        self.ship_name = ship_name
        self.year_construction = year_construction


class PassengersShips(Ship):
    def __init__(self, ship_name, year_construction, total_passengers):
        super().__init__(ship_name, year_construction)
        self.totalPassengers = total_passengers


class CargoShips(Ship):
    def __init__(self, ship_name, year_construction, ship_class, ship_power):
        super().__init__(ship_name, year_construction)
        self.shipClass = ship_class
        self.shipPower = ship_power
