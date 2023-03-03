from Model.Overworld.Overworld import Overworld
from Model.Overworld.Location import Location
class Game():
    def __init__(self, screen):
        self.max_location = 5
        self.screen = screen
        self.overworld = Overworld(0, self.max_location, self.screen, self.createLocation)
        self.screen_status = 'overworld'

    def createLocation(self, current_location):
        self.location = Location(current_location, self.screen, self.createOverworld)
        self.screen_status = 'level'

    def createOverworld(self, current_location, new_max_location):
        if new_max_location > self.max_location:
            self.max_location = new_max_location
        self.overworld = Overworld(current_location, self.max_location, self.screen, self.createLocation)
        self.screen_status = 'overworld'
    def run(self):
        if self.screen_status == 'overworld':
            self.overworld.run()
        else:
            self.location.run()