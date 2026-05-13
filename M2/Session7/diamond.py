class Shape:
    def draw(self):
        print("class shape")


class Circle(Shape):
    def draw(self):
        print("class circle")


class Square(Shape):
    def draw(self):
        print("class square")


class Cylinder(Circle, Square):
    pass


obj = Cylinder()
obj.draw()  # Resolves using the MRO
print(Cylinder.mro())  # Displays the MRO

print(issubclass(Cylinder, object))
print(issubclass(Cylinder, type))
