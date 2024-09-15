from typing import Optional
from ursina import Ursina, camera, random, Entity, destroy, application, Vec3, color, Text, scene #type: ignore
from Clases.Player import Player
from Clases.Enemy import Enemy
from Clases.Coin import Coin
from Clases.Tree import Tree
from Clases.Ground import Ground

#region Variables
coins:list = []
trees:list = []
app = Ursina(borderless=False) # Instanciar el juego
ground = Ground(50) # Instanciar el terreno
player = Player(position=(-5, 0.5, 0)) # Instanciar al jugador
enemy = Enemy(position=(0, 0.75, 0)) # Instanciar al enemigo
#endregion

#region Principal Methods

def create_game():
    tree_generator(50)
    coin_generator(20)


# Función para verificar la recolección de monedas
def update():
    for coin in coins:
        if coin.intersects(player).hit:
            counter.text = int(counter.text) + 1
            destroy(coin)
            coins.remove(coin)
            if not coins:
                pass
    
 #Detección de colisión con el enemigo
    if enemy.intersects(player).hit:
        player.hits += 1
        # Mover al enemigo lejos del jugador después de un hit
        enemy.position = Vec3(random.uniform(-10, 10), enemy.position.y, random.uniform(-10, 10))
        # if player.hits >= 2:
        #     show_game_over(f"¡PLAYER {player.player_number} PERDIÓ!")

    # Ajustar la cámara    
    # camera.position = (player.position.x, 35, player.position.z - 20)
    camera.look_at(player.position)

#endregion

#region Auxiliar Methods

# Función para ajustar la cámara con la rueda del ratón
def camera_adjust(key):
    global camera
    if key == 'scroll up':  # Acercar la cámara
        camera.position += Vec3(0, 5, 5)  # Ajustar el valor según prefieras la velocidad de zoom
    elif key == 'scroll down':  # Alejar la cámara
        camera.position += Vec3(0, -5, -5)

# Generar árboles aleatorios
def tree_generator(tree_numer):
    for _ in range(tree_numer):
        x = random.uniform(-20, 20)
        z = random.uniform(-20, 20)
        trees.append(Tree(position=(x, 1.5, z)))

# Generar monedas aleatorias
def coin_generator(coin_number):   
    for _ in range(coin_number):
        x = random.uniform(-20, 20)
        z = random.uniform(-20, 20)        
        coins.append(Coin(position=(x, 0.5, z)))

#Crea una etiqueta de texto para ponerla en pantalla
def create_Text(text:str, position:Optional[tuple]= None, scale:int = 1, color:color = color.black, background:bool=False):
    return Text(text, origin = position, scale = scale, color = color, background = background)

#endregion

# Contador
counterText = create_Text("Monedas Totales: ", (1.5, -8.5), 2, color.black)
counter = create_Text("0", (9,-5.7), 3, color.white)


# Configurar la cámara
# camera.parent = player
camera.position = (0, 35, -15)
camera.rotation_x = 30

create_game()

app.run()
