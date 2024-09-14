from ursina import Entity, random

tree_texture = 'tree_texture.png'

# Clase Árbol
class Tree(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            texture=tree_texture,
            position=position,
            scale=(1, random.uniform(2, 4), 1),
            collider='box')