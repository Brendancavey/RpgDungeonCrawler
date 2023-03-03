from Model.Overworld.Overworld import Overworld
class Game():
    def __init__(self, screen):
        self.max_location = 2
        self.screen = screen
        self.overworld = Overworld(0, self.max_location, self.screen)


    def run(self):
        self.overworld.run()