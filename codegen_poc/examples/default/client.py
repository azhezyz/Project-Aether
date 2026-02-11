from src_gen import Person, Driver, Car, Wheel, LicencePlate

# Create objects
p = Person()
d = Driver()  # Driver(Person)
car = Car()
plate = LicencePlate()
w1, w2, w3, w4 = Wheel(), Wheel(), Wheel(), Wheel()

# Link associations (based on model labels)
d.drives = car

# Car has (N) Wheel
car.add_has_wheel(w1)
car.add_has_wheel(w2)
car.add_has_wheel(w3)
car.add_has_wheel(w4)

# Car has (1) Licence plate
car.has_licenceplate = plate  # disambiguated attribute name: has_licenceplate

print("Driver drives:", type(d.drives).__name__)
print("Car wheels:", len(car.has_wheel))
print("Car plate:", type(car.has_licenceplate).__name__)
