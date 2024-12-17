class Collider:
    def __init__(self, entity, world):
        self.entity = entity
        self.world = world
        self.world.map = world.map
        
        self.result = []

    def check_x(self):
        if self.left_border_reached() or self.right_border_reached():
            return
        
        if self.entity.get_pos_index().y + 2 >= len(self.world.map):
            return

        rows = [
            self.world.map[self.entity.get_pos_index().y],
            self.world.map[self.entity.get_pos_index().y + 1],
            self.world.map[self.entity.get_pos_index().y + 2],
        ]
      
        for row in rows:
            tiles = row[self.entity.get_pos_index().x : self.entity.get_pos_index().x + 2]
            for tile in tiles:
                if tile.rect is not None:
                    if self.entity.rect.colliderect(tile.rect):
                        if self.entity.velocity.x > 0:
                            self.entity.rect.right = tile.rect.left
                            self.entity.velocity.x = 0
                        if self.entity.velocity.x < 0:
                            self.entity.rect.left = tile.rect.right
                            self.entity.velocity.x = 0

    def check_y(self):
        self.entity.on_ground = False

        if self.entity.get_pos_index().y + 2 >= len(self.world.map):
            return
        
        rows = [
            self.world.map[self.entity.get_pos_index().y],
            self.world.map[self.entity.get_pos_index().y + 1],
            self.world.map[self.entity.get_pos_index().y + 2],
        ]        
        for row in rows:
            tiles = row[self.entity.get_pos_index().x:self.entity.get_pos_index().x+2]
            for tile in tiles:
                if tile.rect is not None:
                    if self.entity.rect.colliderect(tile.rect):
                        if self.entity.velocity.y > 0:
                            self.entity.on_ground = True
                            self.entity.rect.bottom = tile.rect.top
                            self.entity.velocity.y = 0

                            # reset jump on bottom
                            if self.entity.traits is not None:
                                if 'jump' in self.entity.traits:
                                    self.entity.traits['jump'].reset()
                                if 'bounce' in self.entity.traits:
                                    self.entity.traits['bounce'].reset()
                                    
                        if self.entity.velocity.y < 0:
                            self.entity.rect.top = tile.rect.bottom
                            self.entity.velocity.y = 0

    def right_border_reached(self):
        if self.entity.get_pos_index().x >= self.world.map_length - 1:
            self.entity.rect.x = (self.world.map_length - 1) * 32
            self.entity.velocity.x = 0
            return True

    def left_border_reached(self):
        if self.entity.rect.x < 0:
            self.entity.rect.x = 0
            self.entity.velocity.x = 0
            return True
