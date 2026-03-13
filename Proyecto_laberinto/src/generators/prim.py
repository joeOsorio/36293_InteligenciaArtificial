# generators/prim.py
"""
Prim's Algorithm (aleatorizado)
================================
Versión aleatorizada del algoritmo de Prim para árboles de expansión mínima.

Idea
----
1. Comienza con una celda aleatoria en el laberinto (en el "árbol").
2. Agrega todas las paredes de esa celda a una lista de "paredes frontera".
3. Mientras haya paredes en la lista:
   a. Elige una pared al azar de la lista.
   b. Si uno de los dos lados de la pared es una celda no visitada (fuera del árbol):
      - Elimina la pared.
      - Agrega la celda al árbol.
      - Añade sus paredes a la lista frontera.
   c. Si ambos lados ya están en el árbol, descarta la pared.

Resultado: laberintos con muchas ramificaciones cortas, textura diferente al DFS.
"""

import random
from maze.maze import Maze
from maze.cell import Cell


class PrimGenerator:
    """Genera laberintos con el algoritmo de Prim aleatorizado."""

    def generate(self, maze: Maze, start_row: int = 0, start_col: int = 0) -> None:
        """Genera el laberinto.

        Parámetros
        ----------
        maze      : Maze – laberinto con todas las paredes activas
        start_row : int  – fila de partida
        start_col : int  – columna de partida
        """
        start_cell = maze.get_cell(start_row, start_col)
        start_cell.visited = True

        # Lista de "paredes candidatas": tuplas (celda_en_árbol, dirección, celda_vecina)
        frontier = self._get_frontier(maze, start_cell)

        while frontier:
            # Elegimos una pared aleatoria
            cell_in, direction, cell_out = random.choice(frontier)
            frontier.remove((cell_in, direction, cell_out))

            if not cell_out.visited:
                # Conectamos: eliminamos la pared entre ambas celdas
                maze.remove_wall_between(cell_in, cell_out)
                cell_out.visited = True
                # Añadimos las nuevas paredes frontera
                frontier.extend(self._get_frontier(maze, cell_out))

        maze.reset_visited()

    def _get_frontier(self, maze: Maze, cell: Cell) -> list:
        """Devuelve las paredes que separan `cell` de vecinos no visitados."""
        result = []
        for direction, neighbor in maze.get_neighbors(cell.row, cell.col):
            if not neighbor.visited:
                result.append((cell, direction, neighbor))
        return result
