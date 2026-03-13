# generators/recursive_backtracker.py
"""
Recursive Backtracker (DFS iterativo)
======================================
Algoritmo de generación de laberintos basado en DFS con retroceso.

Idea
----
1. Parte de una celda aleatoria y la marca como visitada.
2. Elige un vecino no visitado al azar, elimina la pared entre ellos y avanza.
3. Si no hay vecinos disponibles, retrocede (backtrack) hasta encontrar uno.
4. Termina cuando todas las celdas han sido visitadas.

Resultado: laberintos con muchos pasajes largos y pocos bucles (solución única).
"""

import random
from maze.maze import Maze


class RecursiveBacktracker:
    """Genera laberintos con el algoritmo Recursive Backtracker (DFS)."""

    def generate(self, maze: Maze, start_row: int = 0, start_col: int = 0) -> None:
        """Genera el laberinto modificando las paredes de la cuadrícula `maze`.

        Parámetros
        ----------
        maze      : Maze    – objeto laberinto ya construido (todas las paredes activas)
        start_row : int     – fila de la celda inicial de generación
        start_col : int     – columna de la celda inicial de generación
        """
        # Pila para el retroceso iterativo (evita recursión profunda en laberintos grandes)
        stack = []
        start_cell = maze.get_cell(start_row, start_col)
        start_cell.visited = True
        stack.append(start_cell)

        while stack:
            current = stack[-1]  # Celda actual = cima de la pila

            # Busca vecinos no visitados
            unvisited = maze.get_unvisited_neighbors(current.row, current.col)

            if unvisited:
                # Elige un vecino aleatorio
                direction, neighbor = random.choice(unvisited)
                # Elimina la pared entre la celda actual y el vecino
                maze.remove_wall_between(current, neighbor)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                # Sin vecinos → retroceder
                stack.pop()

        # Limpiamos los flags de visita para que los solvers empiecen desde cero
        maze.reset_visited()
