# agents/agent.py
"""
Agent (clase base abstracta)
==============================
Define la interfaz común que todos los agentes deben implementar.

Diseño
------
- Cada agente tiene acceso al laberinto y una posición actual.
- El método `step()` avanza UN paso del algoritmo.
  Esto permite la visualización fotograma a fotograma.
- `is_done()` indica si el agente llegó a la meta o agotó las opciones.
- `get_path()` devuelve el camino construido hasta el momento.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from maze.maze import Maze


class Agent(ABC):
    """Agente base abstracto para resolver laberintos.

    Parámetros
    ----------
    maze : Maze – laberinto a resolver
    """

    def __init__(self, maze: Maze):
        self.maze = maze
        # Posición actual del agente (fila, columna)
        self.position: Tuple[int, int] = maze.start
        # Número de celdas exploradas (métrica)
        self.nodes_visited: int = 0
        # Indica si el agente terminó (llegó a la meta o no hay solución)
        self._done: bool = False
        # Indica si encontró la meta exitosamente
        self.solved: bool = False

    @abstractmethod
    def step(self) -> None:
        """Ejecuta UN paso del algoritmo de búsqueda.

        Modifica `self.position` y el estado de las celdas.
        Establece `self._done = True` cuando termina.
        """

    @abstractmethod
    def get_path(self) -> List[Tuple[int, int]]:
        """Devuelve la lista de coordenadas (fila, col) que forman el camino
        desde el inicio hasta la posición actual (o la meta si ya llegó)."""

    def is_done(self) -> bool:
        """True si el algoritmo terminó (con éxito o sin solución)."""
        return self._done

    def reset(self) -> None:
        """Reinicia el agente al estado inicial para volver a ejecutar."""
        self.maze.reset_visited()
        self.position = self.maze.start
        self.nodes_visited = 0
        self._done = False
        self.solved = False
        self._reset_internal_state()

    def _reset_internal_state(self) -> None:
        """Subclases pueden sobreescribir para reiniciar estructuras internas."""

    def _mark_path(self, path: List[Tuple[int, int]]) -> None:
        """Marca las celdas del camino final con `in_path = True`."""
        for row, col in path:
            self.maze.get_cell(row, col).in_path = True
