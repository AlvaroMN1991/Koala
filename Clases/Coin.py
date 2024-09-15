from ursina import Entity #type: ignore

coin_texture = 'coin-texture.png'
coin_model = "coin.obj"

# Clase Moneda
class Coin(Entity):
    def __init__(self, position):
        super().__init__(
            model=coin_model,
            texture=coin_texture,
            position=position,
            collider='box',
            rotation_x=90,
            scale=0.5)    
        