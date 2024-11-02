import pygame
import sys

def check_quit():
    """Vérifie si l'utilisateur souhaite fermer l'application."""
    try :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    except :
        pass

def FIN():
    while 1 :
        try :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        except :
            break

class struct:
    """Structure de données simplifiée pour stocker des attributs."""
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __repr__(self):
        return 'struct(' + ', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()]) + ')'