import pygame
import pygame.freetype
from pygame.locals import *
from winsound import Beep
from .utils import *
import tkinter as tk
import atexit, turtle
TURTLE = True

def safe_update():
    try:
        turtle.update()
    except turtle.Terminator:
        # Ignore l'erreur et évite que le programme plante
        pass

# Global constants
THE_SCREEN = None
THE_LEVEL_OF_ZOOM = 4
THE_GRID = False
is_clicking = False

def sleep(time: float):
    """Pauses execution for a specified duration in seconds.
    
    Args:
        time (float): Duration in seconds.
    """
    pygame.time.delay(int(time * 1000))
    if TURTLE :
        safe_update()
    check_quit()


def beep(duration: float, frequency: int):
    """Plays a beep sound with specified duration and frequency.
    
    Args:
        duration (float): Duration of the beep in seconds.
        frequency (int): Frequency of the beep in hertz.
    """
    Beep(frequency, int(duration * 1000))
    check_quit()

def draw_grid():
    """Draws a grid on the screen to help visualize cells."""
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
    """Initializes the display window and draws grid if enabled.
    
    Args:
        largeur (int): Window width.
        hauteur (int): Window height.
        zoom (int): Zoom level for the grid.
        grille (bool): Enable or disable grid.
    """
    if zoom == 0 : zoom = int(282 / max(largeur, hauteur))
    zoom += zoom == 0 
    global THE_SCREEN, THE_LEVEL_OF_ZOOM, THE_GRID
    THE_LEVEL_OF_ZOOM = zoom
    pygame.init()
    pygame.display.set_caption("Pixels Codeboot")
    THE_SCREEN = pygame.display.set_mode((largeur * zoom, hauteur * zoom))
    THE_SCREEN.fill((0, 0, 0))

    if grille:
        draw_grid()
        THE_GRID = True

    pygame.display.flip()
    check_quit()

setScreenMode = set_screen_mode


def fill_rectangle(x: int, y: int, largeur: int, hauteur: int, couleur: str):
    """Fills a rectangle with a specified color in #RGB format.
    
    Args:
        x (int): X position of the rectangle.
        y (int): Y position of the rectangle.
        largeur (int): Width of the rectangle.
        hauteur (int): Height of the rectangle.
        couleur (str): Color in #RGB format.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    if len(couleur) == 4 and couleur[0] == '#':
        r = int(couleur[1] * 2, 16)
        g = int(couleur[2] * 2, 16)
        b = int(couleur[3] * 2, 16)
        couleur_rgb = (r, g, b)
    else:
        raise ValueError("Color must be in #RGB format")

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


def draw_image(x: int, y: int, temp : str):
    """Draws an image based on hexadecimal data formatted in #RGB.
    
    Args:
        x (int): Starting X position.
        y (int): Starting Y position.
        image (str): String containing image data in #RGB format.
    """
    image = temp.replace("    ", "#000")
    rows = image.strip().split('\n')
    for i, row in enumerate(rows):
        colors = [color for color in row.split('#') if len(color) == 3]
        for j, color in enumerate(colors):
            fill_rectangle(x + j, y + i, 1, 1, f'#{color}')

drawImage = draw_image

def set_pixel(x: int, y: int, couleur: str):
    """Sets the color of a pixel at a given position.
    
    Args:
        x (int): X position of the pixel.
        y (int): Y position of the pixel.
        couleur (str): Pixel color in #RGB format.
    """
    fill_rectangle(x, y, 1, 1, couleur)

setPixel = set_pixel

def draw_text(x, y, text, color="#fff", background="#000", scale=1):
    """Draws text on the pixel grid with specified color and background.
    
    Args:
        x (int): X position of the text.
        y (int): Y position of the text.
        text (str): Text to display.
        color (str): Text color in #RGB format.
        background (str): Background color in #RGB format.
        scale (int): Text scale factor.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM

    # Convert RGB444 colors to Pygame format
    def rgb444_to_rgb(color):
        r = int(color[1] * 2, 16)
        g = int(color[2] * 2, 16)
        b = int(color[3] * 2, 16)
        return (r, g, b)

    text_color = rgb444_to_rgb(color)
    bg_color = rgb444_to_rgb(background)

    pygame.freetype.init()
    font_size = 16 * scale  # Font size adjusted by scale factor
    font = pygame.freetype.SysFont(None, font_size)  # Use default Pygame font

    # Draw text in one go
    text_surface, _ = font.render(text, fgcolor=text_color, bgcolor=bg_color)
    text_surface = pygame.transform.scale(text_surface, 
        (text_surface.get_width() // THE_LEVEL_OF_ZOOM, 
         text_surface.get_height() // THE_LEVEL_OF_ZOOM))

    # Calculate position based on x, y and zoom factor
    char_x = x * THE_LEVEL_OF_ZOOM
    char_y = y * THE_LEVEL_OF_ZOOM

    # Draw text on screen
    THE_SCREEN.blit(text_surface, (char_x, char_y))

    # Update display WITHOUT resetting
    pygame.display.update()
    if THE_GRID:
        draw_grid()

    check_quit()
    
drawText = draw_text

def export_screen():
    """Returns a text representation of the current pixel grid state.
    Each line of text contains grid colors in RGB444 format, separated by '\n'.
    
    Returns:
        str: Text representation of the screen content.
    """
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    largeur, hauteur = THE_SCREEN.get_size()
    largeur //= THE_LEVEL_OF_ZOOM
    hauteur //= THE_LEVEL_OF_ZOOM

    def rgb_to_rgb444(color):
        return '#' + ''.join(f'{(c // 17):x}' for c in color)  # Convert to RGB444

    # Traverse grid to get color of each pixel
    rows = []
    for y in range(hauteur):
        row_colors = []
        for x in range(largeur):
            # Get pixel color in (R, G, B) format
            pixel_color = THE_SCREEN.get_at((x * THE_LEVEL_OF_ZOOM + THE_LEVEL_OF_ZOOM // 2,
                                               y * THE_LEVEL_OF_ZOOM + THE_LEVEL_OF_ZOOM // 2))[:3]  # Use pixel center
            # Convert to RGB444
            row_colors.append(rgb_to_rgb444(pixel_color))
        rows.append(''.join(row_colors))

    return '\n'.join(rows)

exportScreen = export_screen

def get_mouse():
    """Gets the mouse position and state, along with modifier key states (Alt, Ctrl, Shift).
    
    This function captures mouse events and returns its coordinates, left button state,
    and information about Alt, Ctrl, and Shift keys. Depending on the turtle_mode parameter,
    it adapts the display method using either the pygame library (for classic event handling)
    or simulating the Turtle environment with Tkinter if pygame fails.

    Returns:
        struct: An object containing mouse coordinates (x, y), button state (left click active or not),
               and Alt, Ctrl, and Shift key states.
    """
    mouse_pos = None
    mouse_button = False
    alt, ctrl, shift = False, False, False
    try :
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_button = True
                    mods = pygame.key.get_mods()
                    alt = bool(mods & pygame.KMOD_ALT)
                    ctrl = bool(mods & pygame.KMOD_CTRL)
                    shift = bool(mods & pygame.KMOD_SHIFT)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click
                    mouse_button = False
        global TURTLE
        TURTLE = False
    except :
        global is_clicking

        def set_clicking(state):
            global is_clicking
            is_clicking = state

        # Screen initialization
        if TURTLE:
            screen = turtle.Screen()
            canvas = screen.getcanvas()
        else:
            root = tk.Tk()
            root.withdraw()  # Hide Tkinter window
            canvas = tk.Canvas(root)
            canvas.pack()

        # Initialize events only once on first call
        if not hasattr(canvas, '_initialized'):
            canvas.bind("<ButtonPress-1>", lambda event: set_clicking(True))
            canvas.bind("<ButtonRelease-1>", lambda event: set_clicking(False))
            canvas._initialized = True  # Mark as initialized to avoid reattaching events

        # Current mouse position
        x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        y = canvas.winfo_pointery() - canvas.winfo_rooty()

        # Convert to Turtle coordinates if Turtle is enabled
        if TURTLE:
            turtle_x = x - canvas.winfo_width() // 2
            turtle_y = -(y - canvas.winfo_height() // 2)
        else:
            turtle_x, turtle_y = x, y  # No conversion if Turtle is disabled

        # Use global variable `is_clicking` for button state
        button = is_clicking

        # If in non-Turtle mode, close window after getting coordinates
        if not TURTLE:
            root.destroy()

        return struct(x=turtle_x, y=turtle_y, button=button, alt=False, ctrl=False, shift=False)

    # If no movement event was detected, use current position
    if mouse_pos is None:
        mouse_pos = pygame.mouse.get_pos()
    
    x, y = mouse_pos
    x, y = x // THE_LEVEL_OF_ZOOM, y // THE_LEVEL_OF_ZOOM  # Adapt to logical size
    
    # Check if mouse is in window
    if x < 0 or y < 0 or x >= THE_SCREEN.get_width() // THE_LEVEL_OF_ZOOM or y >= THE_SCREEN.get_height() // THE_LEVEL_OF_ZOOM:
        x, y = -1, -1  # Invalid position if mouse is outside frame
    
    # If button state hasn't changed, use current state
    if not mouse_button:
        mouse_button = pygame.mouse.get_pressed()[0]
    check_quit()
    return struct(x=x, y=y, button=mouse_button, alt=alt, ctrl=ctrl, shift=shift)

getMouse = get_mouse


def get_mouse_x() :
    """Returns the current X coordinate of the mouse."""
    return get_mouse().x

getMouseX = get_mouse_x

def get_mouse_y() :
    """Returns the current Y coordinate of the mouse."""
    return get_mouse().y

getMouseY = get_mouse_y

def get_mouse_button() :
    """Returns the current state of the mouse button (True if pressed)."""
    return get_mouse().button

getMouseButton = get_mouse_button

def get_mouse_alt() :
    """Returns the current state of the Alt key (True if pressed)."""
    return get_mouse().alt

getMouseAlt = get_mouse_alt

def get_mouse_ctrl() :
    """Returns the current state of the Ctrl key (True if pressed)."""
    return get_mouse().ctrl

getMouseCtrl = get_mouse_ctrl

def get_mouse_shift() :
    """Returns the current state of the Shift key (True if pressed)."""
    return get_mouse().shift

getMouseShift = get_mouse_shift

def get_screen_width():
    """Returns the current width of the grid in cells."""
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    return (THE_SCREEN.get_width() // THE_LEVEL_OF_ZOOM) - 2

getScreenWidth = get_screen_width

def get_screen_height():
    """Returns the current height of the grid in cells."""
    global THE_SCREEN, THE_LEVEL_OF_ZOOM
    return (THE_SCREEN.get_height() // THE_LEVEL_OF_ZOOM) - 2

getScreenHeight = get_screen_height

atexit.register(FIN)