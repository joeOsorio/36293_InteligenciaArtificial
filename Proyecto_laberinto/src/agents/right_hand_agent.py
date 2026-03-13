# agents/right_hand_agent.py
"""
Right Hand Rule Agent – Seguidor de la pared derecha
======================================================
Algoritmo heurístico clásico: el agente siempre intenta girar a la derecha.
Si no puede, avanza recto. Si no puede, gira a la izquierda. Si no puede, retrocede.

Prioridad de movimiento (relativa a la dirección actual):
  1. Derecha → 2. Recto → 3. Izquierda → 4. Atrás

Limitaciones
------------
- Garantiza salida solo si el laberinto es SIMPLEMENTE CONEXO (sin islas internas).
- En laberintos con bucles o islas puede quedar atrapado en un bucle.
- No siempre encuentra el camino MÁS CORTO.
"""

from typing import List, Tuple, Dict
from .agent import Agent
from maze.maze import Maze


class RightHandAgent(Agent):
    """Agente que usa la regla de la mano derecha para navegar el laberinto."""

    # Orden de las direcciones en sentido horario
    DIR_ORDER = ['N', 'E', 'S', 'W']

    # Giros relativos
    TURN_RIGHT = 1    # +1 posición en DIR_ORDER
    TURN_LEFT  = -1   # -1 posición en DIR_ORDER
    TURN_BACK  = 2    # +2 posiciones = media vuelta

    def __init__(self, maze: Maze):
        super().__init__(maze)
        # Comenzamos mirando al Norte
        self.facing: str = 'N'
        # Camino recorrido (para estadísticas y visualización)
        self._path: List[Tuple[int, int]] = [maze.start]
        # Límite de pasos para evitar bucles infinitos
        self.max_steps = maze.rows * maze.cols * 10
        self._steps_taken = 0

        sr, sc = maze.start
        maze.get_cell(sr, sc).visited = True

    def step(self) -> None:
        """Intenta avanzar un paso usando la regla de la mano derecha."""
        if self._done:
            return

        self._steps_taken += 1
        if self._steps_taken > self.max_steps:
            # Límite de seguridad: el laberinto puede no ser simplemente conexo
            self._done = True
            return

        row, col = self.position

        # Intentamos las 4 direcciones en orden: derecha, recto, izquierda, atrás
        for turn in [self.TURN_RIGHT, 0, self.TURN_LEFT, self.TURN_BACK]:
            new_dir = self._turn(self.facing, turn)
            cell = self.maze.get_cell(row, col)

            if not cell.has_wall(new_dir):
                # Podemos ir en esta dirección
                dr, dc = self.maze.DIRECTIONS[new_dir]
                self.facing = new_dir
                self.position = (row + dr, col + dc)
                self._path.append(self.position)
                self.nodes_visited += 1

                nr, nc = self.position
                self.maze.get_cell(nr, nc).visited = True

                if self.position == self.maze.goal:
                    self._done = True
                    self.solved = True
                    self._mark_path(self._path)
                return

    def get_path(self) -> List[Tuple[int, int]]:
        """Devuelve el camino completo recorrido (puede tener retrocesos)."""
        return list(self._path)

    def _turn(self, current_dir: str, delta: int) -> str:
        """Rota la dirección `current_dir` en `delta` pasos (horario)."""
        idx = self.DIR_ORDER.index(current_dir)
        return self.DIR_ORDER[(idx + delta) % 4]

    def _reset_internal_state(self) -> None:
        self.facing = 'N'
        self._path = [self.maze.start]
        self._steps_taken = 0
        sr, sc = self.maze.start
        self.maze.get_cell(sr, sc).visited = True
