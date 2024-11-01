from turtle import * 
def clear(): 
    reset() 
    delay(0) 
    speed(0)

from pymsgbox import *

class struct:
    """Structure de données simplifiée pour stocker des attributs."""
    def __init__(self, **fields):
        self.__dict__.update(fields)

    def __repr__(self):
        return 'struct(' + ', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()]) + ')'