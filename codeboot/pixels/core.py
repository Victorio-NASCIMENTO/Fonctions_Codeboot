import pygame
import pygame.freetype
from pygame.locals import *
from winsound import Beep
from .utils import *

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
    check_quit()

drawGrid = draw_grid

def set_screen_mode(largeur: int, hauteur: int, zoom: float = 0, grille: bool = False):
    """Initialise la fenêtre d'affichage et dessine la grille si activée.
    
    Args:
        largeur (int): Largeur de la fenêtre.
        hauteur (int): Hauteur de la fenétre.
        zoom (int): Niveau de zoom pour la grille.
        grille (bool): Active ou désactive la grille.
    """
    if zoom == 0 : zoom = int(282 / max(largeur, hauteur))
    zoom += zoom == 0 
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

setScreenMode = set_screen_mode


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
    
fillRectangle = fill_rectangle


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

drawImage = draw_image

def set_pixel(x: int, y: int, couleur: str):
    """Définit la couleur d'un pixel à une position donnée.
    
    Args:
        x (int): Position x du pixel.
        y (int): Position y du pixel.
        couleur (str): Couleur du pixel au format #RGB.
    """
    fill_rectangle(x, y, 1, 1, couleur)

setPixel = set_pixel

def draw_text(x, y, text, color="#fff", background="#000", scale=1):
    """
    Dessine du texte sur la grille de pixels, avec une couleur et un arrière-plan définis.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM

    # Convertir les couleurs RGB444 au format Pygame
    def rgb444_to_rgb(color):
        r = int(color[1] * 2, 16)
        g = int(color[2] * 2, 16)
        b = int(color[3] * 2, 16)
        return (r, g, b)

    text_color = rgb444_to_rgb(color)
    bg_color = rgb444_to_rgb(background)

    # Initialiser Pygame FreeType pour le texte
    pygame.freetype.init()
    font_size = 16 * scale  # Taille de police ajustée par le facteur scale
    font = pygame.freetype.SysFont(None, font_size)  # Utilise la police par défaut de Pygame

    # Dessiner le texte en une seule fois
    text_surface, _ = font.render(text, fgcolor=text_color, bgcolor=bg_color)
    text_surface = pygame.transform.scale(text_surface, 
        (text_surface.get_width() // THE_LEVEL_OF_ZOOM, 
         text_surface.get_height() // THE_LEVEL_OF_ZOOM))

    # Calculer la position en fonction de x, y et du facteur de zoom
    char_x = x * THE_LEVEL_OF_ZOOM
    char_y = y * THE_LEVEL_OF_ZOOM

    # Dessiner le texte sur l'écran
    THE_SCREEN.blit(text_surface, (char_x, char_y))

    # Mettre à jour l'affichage SANS réinitialiser
    pygame.display.update()
    if THE_GRID:
        draw_grid()

    check_quit()
    
drawText = draw_text

def export_screen():
    """
    Retourne une représentation textuelle de l'état actuel de la grille de pixels.
    Chaque ligne de texte contient les couleurs de la grille en format RGB444, séparées par des '\n'.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    largeur, hauteur = THE_SCREEN.get_size()
    largeur //= THE_LEVEL_OF_ZOOM
    hauteur //= THE_LEVEL_OF_ZOOM

    def rgb_to_rgb444(color):
        return '#' + ''.join(f'{(c // 17):x}' for c in color)  # Conversion en RGB444

    # Parcourir la grille pour récupérer la couleur de chaque pixel
    rows = []
    for y in range(hauteur):
        row_colors = []
        for x in range(largeur):
            # Obtenir la couleur du pixel au format (R, G, B)
            pixel_color = THE_SCREEN.get_at((x * THE_LEVEL_OF_ZOOM + THE_LEVEL_OF_ZOOM // 2,
                                               y * THE_LEVEL_OF_ZOOM + THE_LEVEL_OF_ZOOM // 2))[:3]  # Utiliser le centre du pixel
            # Convertir en RGB444
            row_colors.append(rgb_to_rgb444(pixel_color))
        rows.append(''.join(row_colors))

    return '\n'.join(rows)

exportScreen = export_screen

def get_mouse():
    # Obtenir et traiter tous les événements de la souris
    mouse_pos = None
    mouse_button = False
    alt, ctrl, shift = False, False, False
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_button = True
                mods = pygame.key.get_mods()
                alt = bool(mods & pygame.KMOD_ALT)
                ctrl = bool(mods & pygame.KMOD_CTRL)
                shift = bool(mods & pygame.KMOD_SHIFT)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Clic gauche
                mouse_button = False
    
    # Si aucun événement de mouvement n'a été détecté, utiliser la position actuelle
    if mouse_pos is None:
        mouse_pos = pygame.mouse.get_pos()
    
    x, y = mouse_pos
    x, y = x // THE_LEVEL_OF_ZOOM, y // THE_LEVEL_OF_ZOOM  # Adapter à la taille logique
    
    # Vérifier si la souris est dans la fenêtre
    if x < 0 or y < 0 or x >= THE_SCREEN.get_width() // THE_LEVEL_OF_ZOOM or y >= THE_SCREEN.get_height() // THE_LEVEL_OF_ZOOM:
        x, y = -1, -1  # Position invalide si la souris est en dehors du cadre
    
    # Si l'état du bouton n'a pas changé, utiliser l'état actuel
    if not mouse_button:
        mouse_button = pygame.mouse.get_pressed()[0]
    
    return struct(x=x, y=y, button=mouse_button, alt=alt, ctrl=ctrl, shift=shift)

getMouse = get_mouse

def get_screen_width():
    """
    Retourne la largeur actuelle de la grille, en nombre de cellules.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    return (THE_SCREEN.get_width() // THE_LEVEL_OF_ZOOM) - 2

getScreenWidth = get_screen_width

def get_screen_height():
    """
    Retourne la hauteur actuelle de la grille, en nombre de cellules.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    return (THE_SCREEN.get_height() // THE_LEVEL_OF_ZOOM) - 2

getScreenHeight = get_screen_height