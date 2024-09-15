from ursina import Entity, random #type: ignore

# Generar el terreno
class Ground(Entity):
    def __init__(self, scale):
        super().__init__(
            model='plane',
            texture='grass',
            collider='box',
            scale=scale
        )