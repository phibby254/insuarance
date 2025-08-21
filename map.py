# here is the town map to find
def paris_map():
    return {
        "Eiffel Tower": (48.8588443, 2.2943506),
        "Louvre Museum": (48.8606111, 2.337644),
        "Notre-Dame Cathedral": (48.853844, 2.349998),
        "Montmartre": (48.8867, 2.3431),
    }

print (paris_map())

class paris_map_class:
    def __init__(self):
        self.map = paris_map()

    def get_location(self, place):
        return self.map.get(place, "Location not found")