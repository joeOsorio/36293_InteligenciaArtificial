# agents/bfs_agent.py
"""
BFS Agent – Breadth First Search
==================================
Explora el laberinto por niveles (olas concéntricas desde el inicio).

Garantiza el CAMINO MÁS CORTO en número de pasos.

Estructura interna
------------------
- queue  : cola FIFO de (fila, col) a explorar
- parent : dict para reconstruir el camino óptimo

Complejidad
-----------
Tiempo  : O(V + E)
Espacio : O(V)  – la cola puede contener todo un nivel del laberinto
"""

from collections import deque
from typing import List, Tuple, Dict, Optional, Deque
from .agent import Agent
from maze.maze import Maze


class BFSAgent(Agent):
    """Agente que resuelve el laberinto con búsqueda en anchura (BFS)."""

    def __init__(self, maze: Maze):
        super().__init__(maze)
        sr, sc = maze.start
        maze.get_cell(sr, sc).visited = True

        # Cola FIFO
        self.queue: Deque[Tuple[int, int]] = deque([maze.start])
        self.parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {
            maze.start: None
        }

    def step(self) -> None:
        """Desencola una celda y añade sus vecinos accesibles no visitados."""
        if self._done:
            return

        if not self.queue:
            self._done = True
            return

        row, col = self.queue.popleft()  # FIFO: el más antiguo primero
        self.position = (row, col)
        self.nodes_visited += 1

        if (row, col) == self.maze.goal:
            self._done = True
            self.solved = True
            self._mark_path(self.get_path())
            return

        for direction, neighbor in self.maze.get_passable_neighbors(row, col):
            n_pos = (neighbor.row, neighbor.col)
            if not neighbor.visited:
                neighbor.visited = True
                self.queue.append(n_pos)
                self.parent[n_pos] = (row, col)

    def get_path(self) -> List[Tuple[int, int]]:
        """Camino óptimo (menor número de pasos) reconstruido desde la meta."""
        path = []
        node: Optional[Tuple[int, int]] = self.maze.goal if self.solved else self.position
        while node is not None:
            path.append(node)
            node = self.parent.get(node)
        path.reverse()
        return path

    def _reset_internal_state(self) -> None:
        sr, sc = self.maze.start
        self.maze.get_cell(sr, sc).visited = True
        self.queue = deque([self.maze.start])
        self.parent = {self.maze.start: None}
