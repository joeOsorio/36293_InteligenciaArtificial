# agents/dfs_agent.py
"""
DFS Agent – Depth First Search
================================
Explora el laberinto yendo siempre lo más profundo posible antes de retroceder.

Estructura interna
------------------
- stack : pila de (fila, col) con las celdas a explorar
- parent : dict que mapea cada celda a su predecesora (para reconstruir el camino)

Complejidad
-----------
Tiempo  : O(V + E)  donde V = celdas, E = pasajes
Espacio : O(V)      en el peor caso la pila tiene todas las celdas
"""

from typing import List, Tuple, Dict, Optional
from .agent import Agent
from maze.maze import Maze


class DFSAgent(Agent):
    """Agente que resuelve el laberinto con búsqueda en profundidad (DFS)."""

    def __init__(self, maze: Maze):
        super().__init__(maze)
        sr, sc = maze.start
        start_cell = maze.get_cell(sr, sc)
        start_cell.visited = True

        # Pila: cada elemento es (fila, col)
        self.stack: List[Tuple[int, int]] = [maze.start]
        # Predecesores para reconstruir el camino al final
        self.parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            maze.start: None
        }

    def step(self) -> None:
        """Extrae una celda de la pila y expande sus vecinos accesibles."""
        if self._done:
            return

        if not self.stack:
            # Sin solución: la pila se vació sin llegar a la meta
            self._done = True
            return

        # Sacamos la cima de la pila
        row, col = self.stack.pop()
        self.position = (row, col)
        self.nodes_visited += 1

        # ¿Llegamos a la meta?
        if (row, col) == self.maze.goal:
            self._done = True
            self.solved = True
            path = self.get_path()
            self._mark_path(path)
            return

        # Expandir vecinos accesibles no visitados
        for direction, neighbor in self.maze.get_passable_neighbors(row, col):
            n_pos = (neighbor.row, neighbor.col)
            if not neighbor.visited:
                neighbor.visited = True
                self.stack.append(n_pos)
                self.parent[n_pos] = (row, col)

    def get_path(self) -> List[Tuple[int, int]]:
        """Reconstruye el camino desde la meta hasta el inicio (orden inverso)."""
        path = []
        node = self.position if not self.solved else self.maze.goal
        while node is not None:
            path.append(node)
            node = self.parent.get(node)
        path.reverse()
        return path

    def _reset_internal_state(self) -> None:
        sr, sc = self.maze.start
        self.maze.get_cell(sr, sc).visited = True
        self.stack = [self.maze.start]
        self.parent = {self.maze.start: None}
