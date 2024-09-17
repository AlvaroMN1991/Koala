#region Imports
from typing import Optional
from ursina import Ursina, camera, random, Entity, destroy, application, Vec3, color, Text, scene, time, DirectionalLight, AmbientLight, Audio, distance #type: ignore
from Clases.Player import Player
from Clases.Enemy import Enemy
from Clases.Coin import Coin
from Clases.Tree import Tree
from Clases.Ground import Ground
from Clases.Heart import Heart
from Clases.GameState import GameState  # Importamos el singleton
#endregion

#region Variables
coins:list = []
trees:list = []
hearts:list = []  # Lista para almacenar los iconos de corazones
app = Ursina(borderless=False) # Instanciar el juego
ground = Ground(50) # Instanciar el terreno
player = Player(position=(-5, 0.75, 0)) # Instanciar al jugador
#enemy = Enemy(position=(0, 0.75, 0)) # Instanciar al enemigo
enemy = Enemy(position=Vec3(random.uniform(-10, 10), 0.75, random.uniform(-10, 10))) # Instanciar al enemigo

# Cargar un sonido
hit_sound = Audio('attack.mp3', autoplay=False)  # Añade la ruta a tu sonido
coin_sound = Audio('coin_collect.mp3', autoplay=False)  # Añade la ruta a tu sonido
base_sound = Audio('base_sound.mp3', autoplay=False, loop=True)  # Añade la ruta a tu sonido
game_over_sound = Audio('death.mp3', autoplay=False)  # Añade la ruta a tu sonido
#endregion

#region Principal Methods

def create_game():
    tree_generator(50)
    coin_generator(20)
    create_hearts(player.lives)
    base_sound.play()  # Reproducir el sonido

# Función para verificar la recolección de monedas
def update():
    #global player_position

    for coin in coins:
        if coin.intersects(player).hit:
            player.coins_collected += 1
            coin_sound.play()  # Reproducir el sonido
            counter.text =str(player.coins_collected)
            destroy(coin)
            coins.remove(coin)
            if not coins:
                pass
    
    # Verificar colisiones con los árboles desde el entorno
    for tree in trees:
        if player.intersects(tree).hit:
             #player.position -= player.move_direction * player.speed * time.dt
            player.position = player.previous_position  # Restaurar la posición anterior
        if enemy.intersects(tree).hit:
            enemy.position = enemy.previous_position  # Restaurar la posición anterior
   
    # Actualizar la posición del jugador en la variable global
    GameState().player_position = player.position
    
      #Detección de colisión con el enemigo
    enemy_attack()
    
    # Ajustar la cámara    
    # camera.position = (player.position.x, 35, player.position.z - 20)
    camera.look_at(player.position)

#endregion

#region Auxiliar Methods

#Función para ver si el enemigo ataca al jugadorcls
def enemy_attack():
    if enemy.intersects(player).hit:
        player.hits += 1
        player.lives -= 1  # Reducir vidas
        hit_sound.play()  # Reproducir el sonido

        # Mover al enemigo lejos del jugador después de un hit
        enemy.position = Vec3(random.uniform(-10, 10), enemy.position.y, random.uniform(-10, 10))
        # if player.hits >= 2:
        #     show_game_over(f"¡PLAYER {player.player_number} PERDIÓ!")
        if player.lives >= 0:
            hearts[player.lives].disable()  # Desactivar un corazón visualmente
        if player.lives == 0:            
            reset_level()  # Reiniciar el nivel cuando no queden vidas

#Función para crear corazones
def create_hearts(lives):
    if len(hearts) > 0:
        for _ in hearts:
            destroy(_)
        hearts.clear()         
    for i in range(lives):
        heart = Heart(i)
        hearts.append(heart)

# Función para ajustar la cámara con la rueda del ratón
def camera_adjust(key):
    global camera
    if key == 'scroll up':  # Acercar la cámara
        camera.position += Vec3(0, 5, 5)  # Ajustar el valor según prefieras la velocidad de zoom
    elif key == 'scroll down':  # Alejar la cámara
        camera.position += Vec3(0, -5, -5)

# Generar árboles aleatorios
def tree_generator(tree_numer):
    if len(trees) > 0:
        for _ in trees:
            destroy(_) 
        trees.clear()
    for _ in range(tree_numer):
        x = random.uniform(-20, 20)
        z = random.uniform(-20, 20)        
        position = Vec3(x, 1.5, z)
        
        while distance(position, player.position) < 2 or distance(position, enemy.position) < 2:
            x = random.uniform(-20, 20)
            z = random.uniform(-20, 20)
            position = Vec3(x, 1.5, z)
        else:
            trees.append(Tree(position=position))

# Generar monedas aleatorias
def coin_generator(coin_number): 
    if len(coins) > 0:
        for _ in coins:
            destroy(_)
        coins.clear()
    for _ in range(coin_number):
        x = random.uniform(-20, 20)
        z = random.uniform(-20, 20)        
        coins.append(Coin(position=(x, 0.5, z)))

#Crea una etiqueta de texto para ponerla en pantalla
def create_Text(text:str, origin:Optional[tuple]= None, position:Optional[tuple]= None, scale:int = 1, color:color = color.black, background:bool=False, parent:Entity=camera.ui):
    return Text(text, origin = origin, position = position, scale = scale, color = color, background = background, parent=parent)

#Función para reiniciar el nivel
def reset_level():
    game_over_sound.play()
    player.lives = 3
    player.coins_collected = 0
    player.position = (0, 0.75, 0)  # Restablecer la posición del jugador
    enemy.position = Vec3(random.uniform(-10, 10), 0.75, random.uniform(-10, 10)) # Instanciar al enemigo  # Restablecer la posición del enemigo
    counter.text =str(player.coins_collected)
    create_hearts(player.lives)  # Volver a mostrar todos los corazones    
    tree_generator(50)
    coin_generator(20)
#endregion



counterText = create_Text("Monedas Totales: ", (0,0), (-0.65, 0.45), 2, color.black) # Contador Texto
counter = create_Text("0", (0,0), (-0.4, 0.45), 3, color.white) #Contador Total
# Configurar la cámara
camera.position = (0, 35, -15)
camera.rotation_x = 30

create_game()

app.run()
