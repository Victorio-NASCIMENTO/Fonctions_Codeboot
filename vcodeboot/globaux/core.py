import math
from random import *
# Turtle Graphics Module

from turtle import *
import atexit
TURTLE = False

def safe_update():
    try:
        update()
    except turtle.Terminator:
        # Ignore l'erreur et évite que le programme plante
        pass

def clear(grid_width=360, grid_height=240):
    """Clear the turtle screen and configure initial settings.

    Args:
        grid_width (int, optional): Width of the grid in pixels. Default is 360.
        grid_height (int, optional): Height of the grid in pixels. Default is 240.
    """
    try:
        reset()
        delay(0) 
        speed(0)
        shape("triangle")
        color("red")
        pencolor("black")
        # Configure turtle mode with custom dimensions if provided
        if grid_width != 360 or grid_height != 240: 
            turtlemode(-1, grid_width, grid_height)
    except:
        raise SystemExit("Program forced to stop.")


def turtlemode(the_speed=-1, grid_width=360, grid_height=240):
    """Configure the turtle environment with a centered grid and white margins.
    
    Args:
        the_speed (int): Speed of the turtle (-1 for instant drawing).
        grid_width (int, optional): Width of the grid in pixels.
        grid_height (int, optional): Height of the grid in pixels.
    """
    TURTLE = True
    tracer(0)  # Set the initial drawing speed to instant

    # Screen configuration
    screen = Screen()
    screen.title("Turtle Codeboot")

    def on_close():
        """Handle screen close event, ensuring proper exit."""
        screen.bye()
        import os
        os._exit(0)  # Use os._exit() to fully exit the program
    
    # Set behavior on window close
    screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)
    
    # Define target dimensions with margin handling for smaller grids
    target_width = grid_width if grid_width is not None else 600
    target_height = grid_height if grid_height is not None else 600
    
    # Add large padding for small window sizes, standard for larger ones
    window_padding = 200 if target_width <= 200 or target_height <= 200 else 100
    
    # Set up initial window size with padding
    screen.setup(width=target_width + window_padding, height=target_height + window_padding)
    screen.cv._rootwindow.resizable(True, True)  # Allow resizing of the window
    screen.bgcolor("white")
    
    def draw_grid(cell_size=20, major_line_every=5, margin=40):
        """Draw a centered grid with configurable cell size and major line frequency.
        
        Args:
            cell_size (int): Size of each grid cell in pixels.
            major_line_every (int): Frequency of thicker lines for major grid lines.
            margin (int): Margin around the grid in pixels.
        """
        # Calculate window dimensions and grid boundaries
        window_width = screen.window_width()
        window_height = screen.window_height()
        
        # Subtract margins to set grid boundaries
        grid_width = window_width - 2 * margin
        grid_height = window_height - 2 * margin
        
        # Center the grid within window boundaries
        half_width = (grid_width // (cell_size * 2)) * cell_size
        half_height = (grid_height // (cell_size * 2)) * cell_size

        # Create a new turtle for grid drawing
        grid_turtle = Turtle()
        grid_turtle.speed(0)
        grid_turtle.color("lightblue")
        grid_turtle.penup()
        
        # Draw horizontal lines
        for y in range(-half_height, half_height + cell_size, cell_size):
            grid_turtle.penup()
            grid_turtle.goto(-half_width, y)
            grid_turtle.pendown()
            grid_turtle.width(2 if y % (cell_size * major_line_every) == 0 else 1)
            grid_turtle.goto(half_width, y)
        
        # Draw vertical lines
        for x in range(-half_width, half_width + cell_size, cell_size):
            grid_turtle.penup()
            grid_turtle.goto(x, -half_height)
            grid_turtle.pendown()
            grid_turtle.width(2 if x % (cell_size * major_line_every) == 0 else 1)
            grid_turtle.goto(x, half_height)
        
        grid_turtle.hideturtle()
    
    # Draw the grid (visible in real-time)
    draw_grid()
    safe_update()
    
    # Set turtle speed for subsequent drawing if specified
    if the_speed != -1:
        speed(the_speed)
        tracer(1)
    shape("triangle")
    color("red")
    pencolor("black")
    atexit.register(done)  # Ensure final screen update upon exit
    atexit.register(update)



from pymsgbox import *

class struct:
    """Simplified data structure for storing attributes."""
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __repr__(self):
        return 'struct(' + ', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()]) + ')'
