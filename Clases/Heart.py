from ursina import Entity, camera #type: ignore

heart_texture = 'heart.png'  # Asegúrate de tener esta imagen

# Clase Enemigo
class Heart(Entity):
    #def __init__(self, game_state, **kwargs):
    def __init__(self, index, **kwargs):
        super().__init__(
            model='quad',
            texture=heart_texture,
            origin=(0,0),
            position=(-0.83 + index * 0.05, 0.38),  # Ajusta la posición para que se alineen horizontalmente
            parent=camera.ui,  # Asegura que los corazones estén en la UI de la cámara y no en el mundo 3D
            scale=(0.05, 0.05),  # Ajusta el tamaño del corazón
            **kwargs)
        