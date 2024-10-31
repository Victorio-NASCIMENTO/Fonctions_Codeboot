import pygame
from pygame.locals import *
from winsound import Beep
from .utils import check_quit, struct

# Constantes globales
THE_SCREEN = None
THE_LEVEL_OF_ZOOM = 4
THE_GRID = False


def sleep(time: float):
    """Fait une pause pour une durée spécifiée en secondes.
    
    Args:
        time (float): Durée en secondes.
    """
    pygame.time.delay(int(time * 1000))
    check_quit()


def beep(duration: float, frequency: int):
    """Joue un bip sonore avec une durée et une fréquence spécifiées.
    
    Args:
        duration (float): Durée du bip en secondes.
        frequency (int): Fréquence du bip en hertz.
    """
    Beep(frequency, int(duration * 1000))
    check_quit()


def draw_grid():
    """Dessine une grille sur l'écran pour aider à visualiser les cellules."""
    gray = (50, 50, 50)
    largeur, hauteur = THE_SCREEN.get_size()
    largeur //= THE_LEVEL_OF_ZOOM
    hauteur //= THE_LEVEL_OF_ZOOM

    for x in range(0, largeur * THE_LEVEL_OF_ZOOM, THE_LEVEL_OF_ZOOM):
        pygame.draw.line(THE_SCREEN, gray, (x, 0), (x, hauteur * THE_LEVEL_OF_ZOOM))

    for y in range(0, hauteur * THE_LEVEL_OF_ZOOM, THE_LEVEL_OF_ZOOM):
        pygame.draw.line(THE_SCREEN, gray, (0, y), (largeur * THE_LEVEL_OF_ZOOM, y))

    pygame.display.flip()


def set_screen_mode(largeur: int, hauteur: int, zoom: int, grille: bool = False):
    """Initialise la fenêtre d'affichage et dessine la grille si activée.
    
    Args:
        largeur (int): Largeur de la fenêtre.
        hauteur (int): Hauteur de la fenétre.
        zoom (int): Niveau de zoom pour la grille.
        grille (bool): Active ou désactive la grille.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM, THE_GRID
    THE_LEVEL_OF_ZOOM = zoom
    pygame.init()
    THE_SCREEN = pygame.display.set_mode((largeur * zoom, hauteur * zoom))
    THE_SCREEN.fill((0, 0, 0))

    if grille:
        draw_grid()
        THE_GRID = True

    pygame.display.flip()
    check_quit()


def fill_rectangle(x: int, y: int, largeur: int, hauteur: int, couleur: str):
    """Remplit un rectangle avec une couleur spécifiée au format #RGB.
    
    Args:
        x (int): Position x du rectangle.
        y (int): Position y du rectangle.
        largeur (int): Largeur du rectangle.
        hauteur (int): Hauteur du rectangle.
        couleur (str): Couleur au format #RGB.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    if len(couleur) == 4 and couleur[0] == '#':
        r = int(couleur[1] * 2, 16)
        g = int(couleur[2] * 2, 16)
        b = int(couleur[3] * 2, 16)
        couleur_rgb = (r, g, b)
    else:
        raise ValueError("Couleur doit être au format #RGB")

    rect = pygame.Rect(
        x * THE_LEVEL_OF_ZOOM,
        y * THE_LEVEL_OF_ZOOM,
        largeur * THE_LEVEL_OF_ZOOM,
        hauteur * THE_LEVEL_OF_ZOOM
    )
    pygame.draw.rect(THE_SCREEN, couleur_rgb, rect)
    pygame.display.update(rect)

    if THE_GRID:
        draw_grid()
    
    check_quit()


def draw_image(x: int, y: int, image: str):
    """Dessine une image basée sur des données hexadécimales formatées en #RGB.
    
    Args:
        x (int): Position x de départ.
        y (int): Position y de départ.
        image (str): Chaéne de caractères contenant les données d'image en format #RGB.
    """
    rows = image.strip().split('\n')
    for i, row in enumerate(rows):
        colors = [color for color in row.split('#') if len(color) == 3]
        for j, color in enumerate(colors):
            fill_rectangle(x + j, y + i, 1, 1, f'#{color}')


def get_mouse():
    """Obtient la position de la souris et l'état du bouton gauche.
    
    Returns:
        struct: Contient x, y, et l'état du bouton.
    """
    mouse_pos = None
    mouse_button = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_button = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                mouse_button = False

    if mouse_pos is None:
        mouse_pos = pygame.mouse.get_pos()

    x, y = mouse_pos
    x, y = x // THE_LEVEL_OF_ZOOM, y // THE_LEVEL_OF_ZOOM

    if x < 0 or y < 0 or x >= THE_SCREEN.get_width() // THE_LEVEL_OF_ZOOM or y >= THE_SCREEN.get_height() // THE_LEVEL_OF_ZOOM:
        x, y = -1, -1

    if not mouse_button:
        mouse_button = pygame.mouse.get_pressed()[0]

    check_quit()
    return struct(x=x, y=y, button=mouse_button)


def set_pixel(x: int, y: int, couleur: str):
    """Définit la couleur d'un pixel à une position donnée.
    
    Args:
        x (int): Position x du pixel.
        y (int): Position y du pixel.
        couleur (str): Couleur du pixel au format #RGB.
    """
    fill_rectangle(x, y, 1, 1, couleur)