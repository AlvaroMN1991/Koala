from ursina import Entity, color, held_keys, time, Vec3 #type: ignore

#Cargar Textura
koala_texture = 'koala_texture.png'
koala_model = "koala.obj"

# Clase Jugador
class Player(Entity):
    #def __init__(self, player_number, game_state, **kwargs):
    def __init__(self, **kwargs):    
        super().__init__(
            model='cube',
            texture=koala_texture,
            collider='box',
            scale=1.5,
            **kwargs)
        #self.player_number = player_number
        self.speed = 5
        self.coins_collected = 0
        self.hits = 0  # Número de veces que el jugador ha sido tocado por el enemigo
        #self.game_state = game_state

        # Asignar teclas de control según el número de jugador
        #if self.player_number == 1:
        self.move_keys = {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd'}
        self.color = color.blue
        #elif self.player_number == 2:
        #    self.move_keys = {'up': 'up arrow', 'down': 'down arrow', 'left': 'left arrow', 'right': 'right arrow'}
        # self.color = color.red

    def update(self):
        #if self.game_state == 'GAME':
            self.move()

    def move(self):
        move_direction = Vec3(
            (held_keys[self.move_keys['right']] - held_keys[self.move_keys['left']]),
            0,
            (held_keys[self.move_keys['up']] - held_keys[self.move_keys['down']])
        ).normalized()
        self.position += move_direction * time.dt * self.speed
