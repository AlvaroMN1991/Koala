from ursina import *
from Clases.Player import Player
from Clases.Enemy import Enemy
from Clases.Coin import Coin
from Clases.Tree import Tree
import random


app = Ursina()

# Variables globales
player1 = None
player2 = None
enemy = None
coins = []
trees = []
num_players = 0
game_state = 'MENU'  # Puede ser 'MENU', 'GAME', 'GAME_OVER'


# Función para crear el terreno, árboles y monedas
def create_game():
    global player1, player2, enemy, coins, trees, game_state

    # Generar el terreno
    ground = Entity(
        model='plane',
        texture='grass',
        collider='box',
        scale=50)

    # Generar árboles aleatorios
    trees = []
    for _ in range(20):
        x = random.uniform(-20, 20)
        z = random.uniform(-20, 20)
        tree = Tree(position=(x, 0.5, z))
        trees.append(tree)

    # Generar monedas aleatorias
    coins = []
    for _ in range(10):
        x = random.uniform(-20, 20)
        z = random.uniform(-20, 20)
        coin = Coin(position=(x, 0.1, z))
        coins.append(coin)

    # Instanciar a los jugadores
    player1 = Player(player_number=1, game_state=game_state, position=(-5, 0.5, 0))
    if num_players == 2:
        player2 = Player(player_number=2, game_state=game_state, position=(5, 0.5, 0))

    # Crear al enemigo
    enemy = Enemy(game_state=game_state, position=(0, 0.75, 0))  # Ajusta la altura según tu modelo

    # Configurar la cámara inicial
    if num_players == 2:
        midpoint = (player1.position + player2.position) / 2
        camera.position = (midpoint.x, 15, midpoint.z - 15)
        camera.look_at(midpoint)
    else:
        camera.position = (player1.position.x, 15, player1.position.z - 15)
        camera.look_at(player1.position)

    game_state = 'GAME'
    
    enemy.game_state = game_state
    player1.game_state = game_state
    if num_players == 2:
        player2.game_state = game_state

# Función para mostrar el menú principal
def show_menu():
    global game_state
    game_state = 'MENU'
    
    # Título
    title = Text(
        text="KOALA GAME",
        origin=(0, 0),
        scale=3,
        color=color.orange,
        background=True
    )

    # Botón 1 Jugador
    button1 = Button(
        text='1 Jugador',
        scale=(0.2, 0.1),
        color=color.azure,
        position=(0, 0.1)
    )
    button1.on_click = lambda: start_game(1)

    # Botón 2 Jugadores
    button2 = Button(
        text='2 Jugadores',
        scale=(0.2, 0.1),
        color=color.azure,
        position=(0, -0.1)
    )
    button2.on_click = lambda: start_game(2)

# Función para iniciar el juego
def start_game(players):
    global num_players
    num_players = players
    destroy_menu()
    create_game()

# Función para destruir el menú
def destroy_menu():
    for e in scene.entities:
        if isinstance(e, Text):
            destroy(e)
        if isinstance(e, Button):
            destroy(e)
        

# Función para mostrar la pantalla de Game Over
def show_game_over(winner_text):
    global game_state
    game_state = 'GAME_OVER'

    player1.game_state = game_state    
    if num_players == 2:
        player2.game_state = game_state

    # Mostrar mensaje de ganador o perdedor
    over_text = Text(
        text=winner_text,
        origin=(0,0),
        scale=2,
        color=color.red,
        background=True
    )
    instruction = Text(
        text="Presiona R para volver al menú",
        origin=(0, -0.2),
        scale=1,
        color=color.white
    )

# Función para reiniciar el juego y volver al menú
def reset_game():
    global player1, player2, enemy, coins, trees, num_players
    # Destruir todas las entidades del juego
    for e in scene.entities:
        if isinstance(e, Player) or isinstance(e, Enemy) or isinstance(e, Coin) or isinstance(e, Tree) or isinstance(e, Entity) and e != camera and e != light:
            destroy(e)
    player1 = None
    player2 = None
    enemy = None
    coins = []
    trees = []
    num_players = 0
    show_menu()

# Función de actualización del juego
def update():
    global game_state

    if game_state == 'GAME':
        # Recolección de monedas
        for player in [player1, player2] if num_players == 2 else [player1]:
            for coin in coins[:]:
                if coin.intersects(player).hit:
                    destroy(coin)
                    coins.remove(coin)
                    player.coins_collected += 1
                    # Verificar si el jugador ha recogido 3 monedas
                    if player.coins_collected >= 3:
                        show_game_over(f"¡WIN PLAYER {player.player_number}!")
        player.game_state = game_state
        enemy.game_state = game_state

        # Detección de colisión con el enemigo
        for player in [player1, player2] if num_players == 2 else [player1]:
            if enemy.intersects(player).hit:
                player.hits += 1
                # Mover al enemigo lejos del jugador después de un hit
                enemy.position = Vec3(random.uniform(-20, 20), enemy.position.y, random.uniform(-20, 20))
                if player.hits >= 2:
                    show_game_over(f"¡PLAYER {player.player_number} PERDIÓ!")
        
        # Ajustar la cámara
        if num_players == 2:
            midpoint = (player1.position + player2.position) / 2
            camera.position = (midpoint.x, 15, midpoint.z - 15)
            camera.look_at(midpoint)
        else:
            camera.position = (player1.position.x, 15, player1.position.z - 15)
            camera.look_at(player1.position)
    
    elif game_state == 'GAME_OVER':
        for player in [player1, player2] if num_players == 2 else [player1]:
            player.game_state = game_state

        enemy.game_state = game_state
        if held_keys['r']:
            reset_game()

# Iniciar el menú al inicio
show_menu()

# Luz para iluminar la escena
light = DirectionalLight()
light.look_at(Vec3(-1, -1, -1))

app.run()
