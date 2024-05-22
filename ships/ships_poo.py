class Ship:
    def __init__(self, ship_name, year_construction):
        self.shipName = ship_name
        self.yearConstruction = year_construction
        self.type = "Cargo"


class PassengersShips(Ship):
    def __init__(self, ship_name, year_construction, total_passengers):
        super().__init__(ship_name, year_construction)
        self.totalPassengers = total_passengers
        self.type = "Passenger"


class CargoShips(Ship):
    def __init__(self, ship_name, year_construction, ship_class, ship_power):
        super().__init__(ship_name, year_construction)
        self.shipClass = ship_class
        self.shipPower = ship_power


class TugShips(Ship):
    def __init__(self, ship_name, year_construction, ship_power, max_speed):
        super().__init__(ship_name, year_construction)
        self.shipPower = ship_power
        self.maxSpeed = max_speed


class TankersShips(Ship):
    def __init__(self, ship_name, year_construction, ship_power, norm_speed, ship_crew):
        super().__init__(ship_name, year_construction)
        self.shipPower = ship_power
        self.normSpeed = norm_speed
        self.shipCrew = ship_crew

