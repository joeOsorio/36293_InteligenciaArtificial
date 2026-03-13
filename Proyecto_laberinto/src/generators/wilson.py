# generators/wilson.py
"""
Wilson's Algorithm (Loop-Erased Random Walk)
=============================================
Genera laberintos mediante caminatas aleatorias sin bucles.

Idea
----
1. Elige cualquier celda como "en el árbol".
2. Mientras queden celdas fuera del árbol:
   a. Elige una celda no visitada al azar como punto de partida.
   b. Realiza una caminata aleatoria hasta llegar al árbol.
   c. Si la caminata forma un bucle, bórralo (loop-erase).
   d. Al llegar al árbol, agrega el camino completo al árbol eliminando las paredes.

Propiedad especial
------------------
Wilson's produce laberintos con distribución UNIFORME sobre todos los árboles
de expansión posibles. Es más lento que DFS o Prim, pero matemáticamente justo.
"""

import random
from maze.maze import Maze


class WilsonGenerator:
    """Genera laberintos con el algoritmo de Wilson (caminata aleatoria sin bucles)."""

    def generate(self, maze: Maze, start_row: int = 0, start_col: int = 0) -> None:
        """Genera el laberinto.

        Parámetros
        ----------
        maze      : Maze – laberinto con todas las paredes activas
        start_row : int  – fila de la primera celda que se agrega al árbol
        start_col : int  – columna de la primera celda
        """
        # Iniciamos el árbol con la celda de inicio
        start_cell = maze.get_cell(start_row, start_col)
        start_cell.visited = True

        # Lista de todas las celdas aún fuera del árbol
        unvisited = [
            maze.get_cell(r, c)
            for r in range(maze.rows)
            for c in range(maze.cols)
            if not maze.get_cell(r, c).visited
        ]

        while unvisited:
            # Celda de partida aleatoria fuera del árbol
            current = random.choice(unvisited)

            # Caminata aleatoria: registramos el camino y la dirección usada
            # path[celda] = dirección usada para salir de esa celda
            path = {current: None}
            walk_order = [current]  # Para mantener el orden del camino

            # Caminar hasta alcanzar el árbol (una celda visitada)
            while not current.visited:
                neighbors = maze.get_neighbors(current.row, current.col)
                direction, next_cell = random.choice(neighbors)

                if next_cell in path:
                    # Loop detectado: borrarlo (loop-erase)
                    loop_start = next_cell
                    # Truncamos walk_order desde loop_start en adelante
                    idx = walk_order.index(loop_start)
                    for cell in walk_order[idx + 1:]:
                        del path[cell]
                    walk_order = walk_order[:idx + 1]
                    current = loop_start
                else:
                    # Avanzar en la caminata
                    path[current] = direction
                    walk_order.append(next_cell)
                    current = next_cell

            # Agregar el camino al árbol eliminando paredes
            for i in range(len(walk_order) - 1):
                cell_a = walk_order[i]
                cell_b = walk_order[i + 1]
                maze.remove_wall_between(cell_a, cell_b)
                cell_a.visited = True
                if cell_a in unvisited:
                    unvisited.remove(cell_a)

        maze.reset_visited()
