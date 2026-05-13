class Cloud:
    def do_something(self):
        print("Cloud something")


class Vehicle:
    pass


class LandVehicle(Vehicle):
    def do_something(self):
        print("Land something")


class TrackedVehicle(LandVehicle):
    def do_something(self):
        print("Tracked something")


class StrutoCamila(Cloud, LandVehicle):
    pass


print(issubclass(TrackedVehicle, object))
print(issubclass(TrackedVehicle, Vehicle))
print(issubclass(TrackedVehicle, LandVehicle))
print(issubclass(TrackedVehicle, Cloud))
print("-" * 40)
print(issubclass(StrutoCamila, object))
print(issubclass(StrutoCamila, Cloud))
print(issubclass(StrutoCamila, Vehicle))
print(issubclass(StrutoCamila, LandVehicle))
print(issubclass(StrutoCamila, TrackedVehicle))

obj = StrutoCamila()

obj.do_something()

print(isinstance(obj, object))
print(isinstance(obj, Cloud))
print(isinstance(obj, StrutoCamila))
