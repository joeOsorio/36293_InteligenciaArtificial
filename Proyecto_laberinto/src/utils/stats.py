# utils/stats.py
"""
Stats
=====
Recopila y formatea las métricas de cada ejecución de un agente.
"""

import time
from typing import Optional


class Stats:
    """Registra métricas de rendimiento de un agente.

    Uso típico
    ----------
    stats = Stats(agent_name="BFS", generator_name="Prim")
    stats.start()
    # ... ejecutar el agente ...
    stats.stop(nodes_visited=42, path_length=18)
    print(stats.summary())
    panel_dict = stats.to_dict()   # Para el panel del renderer
    """

    def __init__(self, agent_name: str = "", generator_name: str = ""):
        self.agent_name     = agent_name
        self.generator_name = generator_name
        self.nodes_visited  = 0
        self.path_length    = 0
        self.elapsed_ms     = 0.0
        self.solved         = False
        self._start_time: Optional[float] = None

    def start(self) -> None:
        """Inicia el cronómetro."""
        self._start_time = time.perf_counter()

    def stop(self, nodes_visited: int, path_length: int, solved: bool = True) -> None:
        """Detiene el cronómetro y almacena las métricas finales."""
        if self._start_time is not None:
            self.elapsed_ms = (time.perf_counter() - self._start_time) * 1000
        self.nodes_visited = nodes_visited
        self.path_length   = path_length
        self.solved        = solved

    def to_dict(self) -> dict:
        """Devuelve un dict listo para mostrar en el panel del Renderer."""
        return {
            "Algoritmo" : self.agent_name,
            "Generador" : self.generator_name,
            "Visitados" : str(self.nodes_visited),
            "Camino"    : str(self.path_length) if self.solved else "---",
            "Tiempo"    : f"{self.elapsed_ms:.1f} ms",
            "Estado"    : "¡Resuelto!" if self.solved else "Sin solución",
        }

    def summary(self) -> str:
        """Cadena de texto para imprimir en consola."""
        lines = [
            f"{'─'*40}",
            f"  Agente    : {self.agent_name}",
            f"  Generador : {self.generator_name}",
            f"  Visitados : {self.nodes_visited}",
            f"  Camino    : {self.path_length if self.solved else 'N/A'}",
            f"  Tiempo    : {self.elapsed_ms:.2f} ms",
            f"  Estado    : {'RESUELTO' if self.solved else 'SIN SOLUCIÓN'}",
            f"{'─'*40}",
        ]
        return "\n".join(lines)
