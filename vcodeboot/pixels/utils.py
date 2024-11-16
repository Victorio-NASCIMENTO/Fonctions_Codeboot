import pygame
import sys

def check_quit():
    """Checks if the user wants to close the application.
    
    Monitors pygame events for quit signals and handles application
    shutdown gracefully if a quit event is detected.
    """
    try :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    except :
        pass

def FIN():
    """Cleanup function that runs at program termination.
    
    Continuously monitors for quit events until pygame can be properly
    shut down. This ensures a clean exit of the application.
    """
    while 1 :
        try :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        except :
            break

class struct:
    """A simplified data structure for storing attributes.
    
    This class provides a simple way to create objects with arbitrary
    attributes, similar to a C struct or a simple data container.
    
    Example:
        data = struct(x=10, y=20)
        print(data.x)  # Outputs: 10
    """
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __repr__(self):
        return 'struct(' + ', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()]) + ')'