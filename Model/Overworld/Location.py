from Controller.GameData import locations

class Location:
    def __init__(self, current_location, surface, create_overworld, remaining_enemies, enemy_locations, visited_locations):
        #location setup
        self.display_surface = surface
        self.current_location = current_location
        location_data = locations[current_location]
        self.location_content = location_data['content']
        self.new_max_location = location_data['unlock']

        #create_overworld method from Game.py
        self.create_overworld = create_overworld

        #enemy overworld data
        self.remaining_enemies = remaining_enemies
        self.enemy_locations = enemy_locations

        #player overworld data
        self.visited_locations = visited_locations

    def run(self):
        if self.location_content:
            self.location_content.interact()
        if not self.location_content.enemy.isAlive():
            print("you win!")
            self.create_overworld(self.current_location, self.new_max_location, self.remaining_enemies, self.enemy_locations, self.visited_locations)





