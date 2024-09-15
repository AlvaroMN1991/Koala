from ursina import Entity, random, time, Vec3 #type: ignore

enemy_texture = 'fireball_with_eyes.png'  # Asegúrate de tener esta imagen

# Clase Enemigo
class Enemy(Entity):
    #def __init__(self, game_state, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube',
            texture=enemy_texture,
            collider='box',
            scale=1.5,
            **kwargs)
        self.speed = 3
        self.direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
        self.change_direction_time = 0  # Tiempo para cambiar de dirección
        #self.game_state = game_state
    
    def update(self):
        #if self.game_state == 'GAME':
            self.move()

    def move(self):
        current_time = time.time()
        # Cambiar de dirección cada 2 segundos
        if current_time > self.change_direction_time:
            self.direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()
            self.change_direction_time = current_time + 2

        self.position += self.direction * time.dt * self.speed

        # Limitar el movimiento dentro del mapa (suelo de 50x50)
        if abs(self.position.x) > 24 or abs(self.position.z) > 24:
            self.direction = Vec3(random.uniform(-1, 1), 0, random.uniform(-1, 1)).normalized()