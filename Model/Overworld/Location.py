from Controller.GameData import locations

class Location:
    def __init__(self, current_location, surface, create_overworld):
        #location setup
        self.display_surface = surface
        self.current_location = current_location
        location_data = locations[current_location]
        self.location_content = location_data['content']
        self.new_max_location = location_data['unlock']
        self.create_overworld = create_overworld


    def run(self):
        self.location_content.commenceBattle()
        self.location_content.update()
        if not self.location_content.enemy.isAlive():
            print("you win!")
            self.create_overworld(self.current_location, self.new_max_location)



