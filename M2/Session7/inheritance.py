class Star:
    def __init__(self, name, galaxy="X"):
        self.name = name
        self.galaxy = galaxy

    def __str__(self) -> str:
        return f"{self.name} // {self.galaxy}"


sun = Star("Sun", "Milky Way")
centauri = Star("A-Cent")

print(sun)
print(centauri)


# Two ways to create a set.
some_set = {centauri, 1, 2, 3, 3, "333"}
the_same_set = set([centauri, 1, 2, 3, 3, 3, 3, 3, "333"])

print(some_set)
print(the_same_set)
