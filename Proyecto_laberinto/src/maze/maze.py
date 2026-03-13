# maze/maze.py
"""
Módulo Maze
===========
Contiene la clase Maze, que gestiona la cuadrícula completa de celdas.
Proporciona métodos para consultar vecinos, eliminar paredes entre celdas
y reiniciar el estado para una nueva búsqueda.
"""

from typing import List, Optional, Tuple
from .cell import Cell


class Maze:
    """Cuadrícula de celdas que representa el laberinto.

    El laberinto se indexa como maze[fila][columna].
    La celda (0, 0) es la esquina superior-izquierda.

    Parámetros
    ----------
    rows : int
        Número de filas del laberinto.
    cols : int
        Número de columnas del laberinto.

    Atributos
    ---------
    rows, cols : int
    grid : list[list[Cell]]  – cuadrícula 2D de celdas
    start : tuple[int, int]  – coordenadas (fila, col) del nodo inicial
    goal  : tuple[int, int]  – coordenadas (fila, col) del nodo objetivo
    """

    # Desplazamientos (delta_fila, delta_col) para cada dirección
    DIRECTIONS = {
        'N': (-1,  0),
        'S': ( 1,  0),
        'E': ( 0,  1),
        'W': ( 0, -1),
    }

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # Construimos la cuadrícula de celdas vacías
        self.grid: List[List[Cell]] = [
            [Cell(r, c) for c in range(cols)]
            for r in range(rows)
        ]
        # Por defecto: inicio en esquina superior-izquierda, meta en inferior-derecha
        self.start: Tuple[int, int] = (0, 0)
        self.goal:  Tuple[int, int] = (rows - 1, cols - 1)

    # ------------------------------------------------------------------
    # Acceso a celdas
    # ------------------------------------------------------------------

    def get_cell(self, row: int, col: int) -> Cell:
        """Devuelve la celda en (row, col). Lanza IndexError si está fuera de rango."""
        if not self.in_bounds(row, col):
            raise IndexError(f"Celda ({row},{col}) fuera del laberinto {self.rows}x{self.cols}")
        return self.grid[row][col]

    def in_bounds(self, row: int, col: int) -> bool:
        """True si (row, col) está dentro de los límites del laberinto."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    # ------------------------------------------------------------------
    # Vecinos
    # ------------------------------------------------------------------

    def get_neighbors(self, row: int, col: int) -> List[Tuple[str, Cell]]:
        """Devuelve todos los vecinos válidos (dentro del laberinto) de (row, col).

        Retorna
        -------
        list of (direction, Cell)
            Incluye TODOS los vecinos, sin importar si hay pared entre ellos.
        """
        neighbors = []
        for direction, (dr, dc) in self.DIRECTIONS.items():
            nr, nc = row + dr, col + dc
            if self.in_bounds(nr, nc):
                neighbors.append((direction, self.grid[nr][nc]))
        return neighbors

    def get_passable_neighbors(self, row: int, col: int) -> List[Tuple[str, Cell]]:
        """Devuelve los vecinos accesibles (sin pared entre ellos) de (row, col).

        Útil para los algoritmos de resolución.
        """
        passable = []
        cell = self.grid[row][col]
        for direction, (dr, dc) in self.DIRECTIONS.items():
            nr, nc = row + dr, col + dc
            if self.in_bounds(nr, nc) and not cell.has_wall(direction):
                passable.append((direction, self.grid[nr][nc]))
        return passable

    def get_unvisited_neighbors(self, row: int, col: int) -> List[Tuple[str, Cell]]:
        """Vecinos válidos aún no visitados. Usado en los generadores."""
        return [
            (d, cell) for d, cell in self.get_neighbors(row, col)
            if not cell.visited
        ]

    # ------------------------------------------------------------------
    # Manipulación de paredes
    # ------------------------------------------------------------------

    def remove_wall_between(self, cell_a: Cell, cell_b: Cell) -> None:
        """Elimina la pared compartida entre dos celdas adyacentes.

        Determina automáticamente la dirección y elimina la pared
        de AMBAS celdas (la pared y su opuesta).
        """
        dr = cell_b.row - cell_a.row
        dc = cell_b.col - cell_a.col

        # Buscamos la dirección correspondiente al desplazamiento
        for direction, (delta_r, delta_c) in self.DIRECTIONS.items():
            if delta_r == dr and delta_c == dc:
                cell_a.remove_wall(direction)
                cell_b.remove_wall(Cell.OPPOSITE[direction])
                return

        raise ValueError(
            f"Las celdas ({cell_a.row},{cell_a.col}) y "
            f"({cell_b.row},{cell_b.col}) no son adyacentes."
        )

    # ------------------------------------------------------------------
    # Estado
    # ------------------------------------------------------------------

    def reset_visited(self) -> None:
        """Reinicia el estado visited e in_path de todas las celdas.

        Llama a esto antes de ejecutar un nuevo algoritmo de resolución
        sin regenerar el laberinto.
        """
        for row in self.grid:
            for cell in row:
                cell.reset_state()

    def reset_all(self) -> None:
        """Reconstruye todas las celdas desde cero (paredes incluidas).

        Útil para regenerar el laberinto con un algoritmo diferente.
        """
        self.grid = [
            [Cell(r, c) for c in range(self.cols)]
            for r in range(self.rows)
        ]

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"Maze({self.rows}x{self.cols}) start={self.start} goal={self.goal}"
