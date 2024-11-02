# Turtle

from turtle import *
import atexit

def clear(): 
        reset() 
        delay(0) 
        speed(0)


def turtlemode():
    tracer(0)
    # Configuration de l'écran
    screen = Screen()
    screen.title("Turtle Codeboot")
    
    # Calculer la largeur proportionnelle pour une hauteur de 600px
    # Pour un écran 16:9, cela donnera une largeur de 1067px environ
    target_height = 600
    aspect_ratio = 16/9  # ratio standard pour les écrans modernes
    target_width = int(target_height * aspect_ratio)
    
    # Configuration initiale de la fenêtre
    screen.setup(width=target_width, height=target_height)
    # Permettre le redimensionnement
    screen.cv._rootwindow.resizable(True, True)
    screen.bgcolor("white")
    
    # Fonction pour dessiner la grille avec des lignes plus épaisses
    def dessiner_grille(cell_size=20, major_line_every=5):
        # Obtenir les dimensions actuelles de la fenêtre
        window_width = screen.window_width()
        window_height = screen.window_height()
        half_width = window_width // 2
        half_height = window_height // 2

        grid_turtle = Turtle()
        grid_turtle.speed(0)
        grid_turtle.color("lightblue")
        grid_turtle.penup()
        
        # Dessiner des lignes horizontales
        for y in range(-half_height, half_height + 1, cell_size):
            grid_turtle.penup()
            grid_turtle.goto(-half_width, y)
            grid_turtle.pendown()
            if y % (cell_size * major_line_every) == 0:
                grid_turtle.width(2)  # Lignes épaisses
            else:
                grid_turtle.width(1)  # Lignes normales
            grid_turtle.goto(half_width, y)
        
        # Dessiner des lignes verticales
        for x in range(-half_width, half_width + 1, cell_size):
            grid_turtle.penup()
            grid_turtle.goto(x, -half_height)
            grid_turtle.pendown()
            if x % (cell_size * major_line_every) == 0:
                grid_turtle.width(2)  # Lignes épaisses
            else:
                grid_turtle.width(1)  # Lignes normales
            grid_turtle.goto(x, half_height)
        
        grid_turtle.hideturtle()
    
    # Dessiner la grille (visible en temps réel)
    dessiner_grille()
    update()
    tracer(1)
    color("red")
    pencolor("black")
    atexit.register(done)



from pymsgbox import *

class struct:
    """Structure de données simplifiée pour stocker des attributs."""
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __repr__(self):
        return 'struct(' + ', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()]) + ')'