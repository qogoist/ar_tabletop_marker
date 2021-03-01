

class Player:
    def __init__(self, player_id, name):
        self.id = player_id
        self.name = name
        self.position = 0
        self.rotation = 0
    
    def __str__(self):
      return "{{ID: {}, Name: {}, Position: {}, Rotation: {}}}".format(self.id, self.name, self.position, self.rotation)

    def __repr__(self):
      return "{{ID: {}, Name: {}, Position: {}, Rotation: {}}}".format(self.id, self.name, self.position, self.rotation)