from ursina import Text, Button, color, destroy #type: ignore


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

def start_game(players):
    global num_players
    num_players = players
    destroy_menu()
    create_game()

# Función para destruir el menú
def destroy_menu(scene):
    for e in scene.entities:
        if isinstance(e, Text):
            destroy(e)
        if isinstance(e, Button):
            destroy(e)
        