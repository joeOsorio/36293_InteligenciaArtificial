# =============================================================
#  agent/bfs_agent.py
#  El Agente BFS — decide cuándo avanzar, a qué velocidad
#  y gestiona el estado de la búsqueda.
#
#  Responsabilidades:
#    - Mantener el índice del paso actual
#    - Controlar play/pausa y velocidad
#    - Responder a eventos de teclado (teclas de control)
#    - Reiniciar la búsqueda con nuevas ciudades
#
#  El agente NO dibuja nada — solo actualiza estado.
#  El renderer consulta al agente para saber qué mostrar.
# =============================================================

from bfs.algorithm  import bfs_steps, get_path_cost
from config.settings import SPEED_MIN, SPEED_MAX, SPEED_INIT


class BFSAgent:
    """
    Agente que ejecuta y controla la animación BFS.

    Atributos públicos (lectura)
    ----------------------------
    inicio      : str   ciudad de origen actual
    meta        : str   ciudad destino actual
    step        : dict  snapshot del paso actual
    step_index  : int   índice dentro de steps
    total_steps : int   cantidad total de pasos generados
    playing     : bool  True si la animación está corriendo
    speed       : int   pasos por segundo
    path_cost   : int   costo en km de la ruta (−1 si no hay)
    """

    def __init__(self, grafo, inicio, meta):
        self._grafo  = grafo
        self.inicio  = inicio
        self.meta    = meta
        self.speed   = SPEED_INIT
        self.playing = False
        self._timer  = 0.0
        self._reset_search()

    # ── Inicialización interna ────────────────────────────────

    def _reset_search(self):
        """(Re)genera los pasos BFS y posiciona en el paso 0."""
        self._steps     = bfs_steps(self._grafo, self.inicio, self.meta)
        self.step_index = 0
        self.playing    = False
        self._timer     = 0.0

    # ── Propiedades derivadas ─────────────────────────────────

    @property
    def step(self):
        return self._steps[self.step_index]

    @property
    def total_steps(self):
        return len(self._steps)

    @property
    def path_cost(self):
        path = self.step.get("path", [])
        if path:
            return get_path_cost(self._grafo, path)
        return -1

    # ── Actualización por frame ───────────────────────────────

    def update(self, dt):
        """
        Llamar una vez por frame con el delta-time en segundos.
        Avanza al siguiente paso si corresponde.
        """
        if not self.playing:
            return
        if self.step_index >= self.total_steps - 1:
            self.playing = False
            return

        self._timer += dt
        if self._timer >= 1.0 / self.speed:
            self._timer = 0.0
            self.step_index += 1
            if self.step_index >= self.total_steps - 1:
                self.playing = False

    # ── Controles ─────────────────────────────────────────────

    def toggle_play(self):
        """Play / Pausa."""
        self.playing = not self.playing

    def step_forward(self):
        """Avanza un paso (pausa automática)."""
        self.playing    = False
        self.step_index = min(self.step_index + 1, self.total_steps - 1)

    def step_backward(self):
        """Retrocede un paso (pausa automática)."""
        self.playing    = False
        self.step_index = max(self.step_index - 1, 0)

    def restart(self):
        """Vuelve al paso 0 sin regenerar los pasos."""
        self.step_index = 0
        self.playing    = False
        self._timer     = 0.0

    def increase_speed(self):
        self.speed = min(self.speed + 1, SPEED_MAX)

    def decrease_speed(self):
        self.speed = max(self.speed - 1, SPEED_MIN)

    def set_cities(self, inicio, meta):
        """
        Cambia origen y/o destino y regenera la búsqueda BFS.

        Parámetros
        ----------
        inicio : str  nueva ciudad de origen
        meta   : str  nueva ciudad destino
        """
        self.inicio = inicio
        self.meta   = meta
        self._reset_search()
