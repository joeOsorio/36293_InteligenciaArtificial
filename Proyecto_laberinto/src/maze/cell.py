# maze/cell.py
"""
Módulo Cell
===========
Define la unidad básica del laberinto: una celda con paredes en 4 direcciones,
estado de visita, y coordenadas (fila, columna).

Estructura de paredes
---------------------
Cada celda tiene un diccionario de booleanos con 4 claves:
    'N' (Norte/arriba), 'S' (Sur/abajo), 'E' (Este/derecha), 'W' (Oeste/izquierda)
True  → la pared EXISTE (celda bloqueada en esa dirección)
False → la pared fue ELIMINADA (hay un pasaje)
"""


class Cell:
    """Representa una celda individual dentro del laberinto.

    Atributos
    ---------
    row : int
        Fila de la celda en la cuadrícula (0 = arriba).
    col : int
        Columna de la celda en la cuadrícula (0 = izquierda).
    walls : dict[str, bool]
        Estado de cada pared. True = existe, False = eliminada.
    visited : bool
        Usado durante la generación y/o resolución del laberinto.
    in_path : bool
        True si la celda forma parte del camino solución final.
    """

    # Dirección opuesta, útil para eliminar la pared del vecino
    OPPOSITE = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        # Todas las paredes activas al inicio
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False   # Para generadores y solvers
        self.in_path = False   # Para marcar el camino final

    def remove_wall(self, direction: str) -> None:
        """Elimina la pared en la dirección dada.

        Parámetros
        ----------
        direction : str
            Una de 'N', 'S', 'E', 'W'.
        """
        self.walls[direction] = False

    def has_wall(self, direction: str) -> bool:
        """Devuelve True si existe pared en esa dirección."""
        return self.walls[direction]

    def reset_state(self) -> None:
        """Reinicia los flags de visita y camino (sin tocar las paredes)."""
        self.visited = False
        self.in_path = False

    def __repr__(self) -> str:
        walls_str = ''.join(d for d, v in self.walls.items() if v)
        return f"Cell({self.row},{self.col}) walls=[{walls_str}]"
