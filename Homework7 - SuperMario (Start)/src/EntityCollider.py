class CollisionState:
    def __init__(self, is_colliding, is_top):
        self.is_colliding = is_colliding
        self.is_top = is_top


class EntityCollider:
    def __init__(self, entity):
        self.entity = entity

    def check(self, target):
        if self.entity.rect.colliderect(target.rect):
            return self.determine_side(target.rect, self.entity.rect)
        return CollisionState(False, False)

    def determine_side(self, rect1, rect2):
        if (rect1.collidepoint(rect2.bottomleft)
            or rect1.collidepoint(rect2.bottomright)
            or rect1.collidepoint(rect2.midbottom)
        ):
            if (rect2.collidepoint((rect1.midleft[0] / 2, rect1.midleft[1] / 2)) 
                or rect2.collidepoint((rect1.midright[0] / 2, rect1.midright[1] / 2))
            ):
                return CollisionState(True, False)
            elif self.entity.velocity.y > 0:
                return CollisionState(True, True)
        return CollisionState(True, False)



