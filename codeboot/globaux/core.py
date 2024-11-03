import math
from random import *
# Turtle

from turtle import *
import atexit
TURTLE = False

def clear(grid_width = 360, grid_height = 240):
        try :
            reset()
            delay(0) 
            speed(0)
            shape("triangle")
            color("red")
            pencolor("black")
            if grid_width != 360 or grid_height != 240 : turtlemode(-1, grid_width, grid_height)
        except :
            raise SystemExit("Arrêt forcé du programme.")


def turtlemode(the_speed=-1, grid_width=360, grid_height=240):
    """Configure l'environnement turtle avec une grille centrée et une marge blanche.
    
    Args:
        the_speed (int): Vitesse de la tortue (-1 pour instantané)
        grid_width (int, optional): Largeur de la grille en pixels
        grid_height (int, optional): Hauteur de la grille en pixels
    """
    TURTLE = True
    tracer(0)
    # Configuration de l'écran
    screen = Screen()
    screen.title("Turtle Codeboot")
    
    # Si dimensions spécifiées, utiliser celles-ci avec une marge suffisante
    if grid_width is not None or grid_height is not None:
        # Utiliser les dimensions spécifiées ou la valeur par défaut de 600
        target_width = grid_width if grid_width is not None else 600
        target_height = grid_height if grid_height is not None else 600
        
        # Ajouter une marge substantielle pour les petites dimensions
        if target_width <= 200 or target_height <= 200:
            window_padding = 200  # Grande marge pour les petites fenêtres
        else:
            window_padding = 100  # Marge standard pour les grandes fenêtres
    else:
        # Dimensions par défaut pour le mode 16:9
        target_height = 600
        aspect_ratio = 16/9
        target_width = int(target_height * aspect_ratio)
        window_padding = 100
    
    # Configuration initiale de la fenêtre avec la marge
    screen.setup(width=target_width + window_padding, height=target_height + window_padding)
    # Permettre le redimensionnement
    screen.cv._rootwindow.resizable(True, True)
    screen.bgcolor("white")
    
    def dessiner_grille(cell_size=20, major_line_every=5, margin=40):
        # Obtenir les dimensions actuelles de la fenêtre
        window_width = screen.window_width()
        window_height = screen.window_height()
        
        # Calculer les limites de la grille en soustrayant la marge désirée
        grid_width = window_width - 2 * margin
        grid_height = window_height - 2 * margin
        
        # Calculer les limites de la grille pour qu'elle soit centrée
        half_width = (grid_width // (cell_size * 2)) * cell_size
        half_height = (grid_height // (cell_size * 2)) * cell_size

        grid_turtle = Turtle()
        grid_turtle.speed(0)
        grid_turtle.color("lightblue")
        grid_turtle.penup()
        
        # Dessiner des lignes horizontales
        for y in range(-half_height, half_height + cell_size, cell_size):
            grid_turtle.penup()
            grid_turtle.goto(-half_width, y)
            grid_turtle.pendown()
            if y % (cell_size * major_line_every) == 0:
                grid_turtle.width(2)
            else:
                grid_turtle.width(1)
            grid_turtle.goto(half_width, y)
        
        # Dessiner des lignes verticales
        for x in range(-half_width, half_width + cell_size, cell_size):
            grid_turtle.penup()
            grid_turtle.goto(x, -half_height)
            grid_turtle.pendown()
            if x % (cell_size * major_line_every) == 0:
                grid_turtle.width(2)
            else:
                grid_turtle.width(1)
            grid_turtle.goto(x, half_height)
        
        grid_turtle.hideturtle()
    
    # Dessiner la grille (visible en temps réel)
    dessiner_grille()
    update()
    if the_speed != -1:
        speed(the_speed)
        tracer(1)
    shape("triangle")
    color("red")
    pencolor("black")
    atexit.register(done)
    atexit.register(update)



from pymsgbox import *

class struct:
    """Structure de données simplifiée pour stocker des attributs."""
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __repr__(self):
        return 'struct(' + ', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()]) + ')'