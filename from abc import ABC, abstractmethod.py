from abc import ABC, abstractmethod
import random
import datetime

class BaseEntity(ABC):
    def __init__(self, _id, name=""):
        self._id = _id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @abstractmethod
    def display_info(self):
        pass


class Car(BaseEntity):
    def __init__(self, _id, license_plate, model, owner=None, mileage=0):
        super().__init__(_id)
        self._license_plate = license_plate
        self._model = model
        self.owner = owner
        self.mileage = mileage 
        self.radar_systems = []

    def get_license_plate(self):
        return self._license_plate

    def set_license_plate(self, plate):
        self._license_plate = plate

    def display_info(self):
        return (f"Car #{self.id}: {self._model} - Plate: {self._license_plate}, "
                f"Owner: {self.owner}, Mileage: {self.mileage} km")


class RadarSystem(BaseEntity):
    def __init__(self, _id, car, radar_type, status="Active", version="v1.0"):
        super().__init__(_id)
        self._car = car
        self._radar_type = radar_type
        self._status = status
        self._version = version
        self.radar_readings = []
        self.alerts = []
        self.maintenance_records = []
        car.radar_systems.append(self)

    def display_info(self):
        return (f"Radar #{self.id} ({self._radar_type}) for car "
                f"{self._car.get_license_plate()} - Status: {self._status}, "
                f"Version: {self._version}")


class RadarReading(BaseEntity):
    def __init__(self, _id, radar_system, distance, speed, timestamp=None):
        super().__init__(_id)
        self._radar_system = radar_system
        self._distance = distance
        self._speed = speed
        self.timestamp = timestamp or "Not Recorded"
        radar_system.radar_readings.append(self)

    def get_speed(self):
        return self._speed

    def get_distance(self):
        return self._distance

    def display_info(self):
        return (f"Reading #{self.id}: Speed = {self._speed} km/h, "
                f"Distance = {self._distance} m, Timestamp: {self.timestamp}")


class Alert(BaseEntity, ABC):
    def __init__(self, _id, radar_system, alert_type, priority="Low"):
        super().__init__(_id)
        self._radar_system = radar_system
        self._alert_type = alert_type
        self._priority = priority  
        self._resolved = False 

    @abstractmethod
    def display_info(self):
        pass

    def resolve(self):
        self._resolved = True

    def display_resolved_status(self):
        return "Resolved" if self._resolved else "Unresolved"


class SpeedAlert(Alert):
    def __init__(self, _id, radar_system, speed_measured, speed_limit, priority="High"):
        super().__init__(_id, radar_system, "Speed Limit Exceeded", priority)
        self._speed_measured = speed_measured
        self._speed_limit = speed_limit
        radar_system.alerts.append(self)

    def display_info(self):
        return (f"ALERT #{self.id}: {self._alert_type} - "
                f"Speed {self._speed_measured} > Limit {self._speed_limit}, "
                f"Priority: {self._priority}, Status: {self.display_resolved_status()}")


class DistanceAlert(Alert):
    def __init__(self, _id, radar_system, distance_measured, min_distance, priority="Medium"):
        super().__init__(_id, radar_system, "Unsafe Distance Detected", priority)
        self._distance_measured = distance_measured
        self._min_distance = min_distance
        radar_system.alerts.append(self)

    def display_info(self):
        return (f"ALERT #{self.id}: {self._alert_type} - "
                f"Distance {self._distance_measured} < Minimum {self._min_distance}, "
                f"Priority: {self._priority}, Status: {self.display_resolved_status()}")


class Technician(BaseEntity):
    def __init__(self, _id, name, email, certification_level="Beginner", department="Tech"):
        super().__init__(_id, name)
        self._email = email
        self.certification_level = certification_level 
        self.department = department 
        self.maintenance_records = []

    def display_info(self):
        return (f"Technician #{self.id}: {self.name} - {self._email}, "
                f"Certification Level: {self.certification_level}, "
                f"Department: {self.department}")


class MaintenanceRecord(BaseEntity):
    def __init__(self, _id, radar_system, technician, notes="", date="Not Set"):
        super().__init__(_id)
        self._radar_system = radar_system
        self._technician = technician
        self._notes = notes
        self._date = date 
        radar_system.maintenance_records.append(self)
        technician.maintenance_records.append(self)

    def display_info(self):
        return (f"Maintenance #{self.id} by {self._technician.name} - "
                f"Notes: {self._notes}, Date: {self._date}")


class SystemReport:
    def __init__(self, root_entity: BaseEntity):
        self.root_entity = root_entity
        self.reported = set()

    def generate_report(self):
        print("=== System Report ===")
        self._traverse(self.root_entity)

    def _traverse(self, entity: BaseEntity):
        if id(entity) in self.reported:
            return
        self.reported.add(id(entity))
        print(entity.display_info())

        if isinstance(entity, Car):
            for radar in entity.radar_systems:
                self._traverse(radar)

        elif isinstance(entity, RadarSystem):
            for reading in entity.radar_readings:
                self._traverse(reading)
            for alert in entity.alerts:
                self._traverse(alert)
            for rec in entity.maintenance_records:
                self._traverse(rec)

        elif isinstance(entity, Technician):
            for record in entity.maintenance_records:
                self._traverse(record)

        elif isinstance(entity, MaintenanceRecord):
            self._traverse(entity._technician)

        elif isinstance(entity, Alert):
            self._traverse(entity._radar_system)

        elif isinstance(entity, RadarReading):
            self._traverse(entity._radar_system)


# === Utility functions to generate random data ===

def generate_random_car():
    models = ["Tesla Model 3", "BMW X5", "Audi A4", "Mercedes-Benz E-Class"]
    plates = ["XYZ-123", "ABC-456", "DEF-789", "GHI-012"]
    owners = ["John Doe", "Jane Smith", "Alice Brown", "Bob White"]
    return Car(
        random.randint(1000, 9999),
        random.choice(plates),
        random.choice(models),
        owner=random.choice(owners),
        mileage=random.randint(1000, 20000)
    )


def generate_random_radar(car):
    types = ["Front Radar", "Rear Radar", "Side Radar"]
    radar = RadarSystem(
        random.randint(1000, 9999),
        car,
        random.choice(types),
        status=random.choice(["Active", "Inactive"]),
        version=f"v{random.randint(1,3)}.{random.randint(0,9)}"
    )
    for _ in range(random.randint(1,5)):
        RadarReading(
            random.randint(1000, 9999),
            radar,
            distance=random.randint(1,100),
            speed=random.randint(50,150),
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    return radar


def generate_random_alert(radar):
    if random.choice([True, False]):
        return SpeedAlert(
            random.randint(1000, 9999),
            radar,
            speed_measured=random.randint(100,200),
            speed_limit=random.randint(60,120),
            priority=random.choice(["High","Medium","Low"])
        )
    else:
        return DistanceAlert(
            random.randint(1000, 9999),
            radar,
            distance_measured=random.randint(5,50),
            min_distance=random.randint(10,100),
            priority=random.choice(["High","Medium","Low"])
        )


def generate_random_maintenance_record(radar, tech):
    return MaintenanceRecord(
        random.randint(1000, 9999),
        radar,
        tech,
        notes=random.choice(["Firmware update","Sensor calibration","System reboot"]),
        date=datetime.datetime.now().strftime("%Y-%m-%d")
    )


if __name__ == "__main__":
    car1 = generate_random_car()
    car2 = generate_random_car()

    radar1 = generate_random_radar(car1)
    radar2 = generate_random_radar(car2)

    tech = Technician(1, "Alice Smith", "alice@example.com", certification_level="Advanced", department="Radar Maintenance")

    alert1 = generate_random_alert(radar1)
    alert2 = generate_random_alert(radar2)

    rec1 = generate_random_maintenance_record(radar1, tech)
    rec2 = generate_random_maintenance_record(radar2, tech)

    report = SystemReport(car1)
    report.generate_report()

    print("\n--- Additional Report for Car 2 ---")
    SystemReport(car2).generate_report()

    print("\n--- Summary ---")
    print(f"Technician {tech.name} has {len(tech.maintenance_records)} maintenance records.")
    print(f"Radar {radar1.id} on car {car1.get_license_plate()} has {len(radar1.radar_readings)} readings.")
    print(f"Radar {radar2.id} on car {car2.get_license_plate()} has {len(radar2.radar_readings)} readings.")
