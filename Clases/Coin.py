from ursina import Entity

coin_texture = 'coin_texture.png'

# Clase Moneda
class Coin(Entity):
    def __init__(self, position):
        super().__init__(
            model='circle',
            texture=coin_texture,
            position=position,
            collider='box',
            rotation_x=90,
            scale=0.5)