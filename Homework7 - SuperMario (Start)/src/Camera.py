from src.Math import Vec2D

class Camera:
    def __init__(self, pos, entity):
        self.pos = Vec2D(pos.x, pos.y)
        self.entity = entity
        self.x = self.pos.x * 32
        self.y = self.pos.y * 32

    def move(self):
        x = self.entity.get_pos_index_as_float().x
        if 10 < x < 50:
            self.pos.x = -x + 10
        self.x = self.pos.x * 32
        self.y = self.pos.y * 32
