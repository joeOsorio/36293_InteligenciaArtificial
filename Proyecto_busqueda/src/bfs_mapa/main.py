# =============================================================
#  main.py
#  Punto de entrada del programa.
#
#  Responsabilidades:
#    - Inicializar pygame y crear la ventana
#    - Cargar fuentes
#    - Instanciar el agente y los renderers
#    - Ejecutar el game-loop principal
#    - Despachar eventos de teclado al agente
# =============================================================

import sys
import pygame

from config.settings import (
    WINDOW_W, WINDOW_H, FPS, TITLE,
    DEFAULT_START, DEFAULT_GOAL,
    FONT_TITLE, FONT_MEDIUM, FONT_SMALL, FONT_EDGE,
)
from graph.map_data        import GRAFO, POSICIONES
from agent.bfs_agent       import BFSAgent
from renderer.graph_renderer  import GraphRenderer
from renderer.panel_renderer  import PanelRenderer
from renderer.city_selector   import show_city_selector


# ── Helpers ───────────────────────────────────────────────────

def _load_fonts():
    """Carga todas las fuentes usadas en el proyecto."""
    def load(cfg):
        name, size, bold = cfg
        return pygame.font.SysFont(name, size, bold=bold)

    return {
        "h":    load(FONT_TITLE),
        "md":   load(FONT_MEDIUM),
        "sm":   load(FONT_SMALL),
        "edge": load(FONT_EDGE),
    }


def _handle_events(event, agent, screen, fonts, cities):
    """
    Procesa un evento pygame y lo traduce en acciones del agente.

    Retorna
    -------
    bool  False si el usuario quiere salir, True en caso contrario.
    """
    if event.type == pygame.QUIT:
        return False

    if event.type != pygame.KEYDOWN:
        return True

    key = event.key

    if key == pygame.K_ESCAPE:
        return False

    elif key == pygame.K_SPACE:
        agent.toggle_play()

    elif key == pygame.K_RIGHT:
        agent.step_forward()

    elif key == pygame.K_LEFT:
        agent.step_backward()

    elif key == pygame.K_r:
        agent.restart()

    elif key == pygame.K_UP:
        agent.increase_speed()

    elif key == pygame.K_DOWN:
        agent.decrease_speed()

    elif key == pygame.K_TAB:
        # Selector de ciudades bloqueante
        nuevo_inicio = show_city_selector(
            screen, cities, "Selecciona ORIGEN",
            fonts["h"], fonts["sm"]
        )
        nuevo_meta = show_city_selector(
            screen, cities, "Selecciona DESTINO",
            fonts["h"], fonts["sm"]
        )
        if nuevo_inicio and nuevo_meta:
            agent.set_cities(nuevo_inicio, nuevo_meta)

    return True


# ── Game loop ─────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption(TITLE)
    clock  = pygame.time.Clock()

    fonts  = _load_fonts()
    cities = sorted(GRAFO.keys())

    # Instanciar módulos
    agent = BFSAgent(GRAFO, DEFAULT_START, DEFAULT_GOAL)

    graph_renderer = GraphRenderer(
        screen     = screen,
        posiciones = POSICIONES,
        grafo      = GRAFO,
        fonts      = {"sm": fonts["sm"], "edge": fonts["edge"]},
    )
    panel_renderer = PanelRenderer(
        screen = screen,
        fonts  = fonts,
    )

    # ── Loop principal ────────────────────────────────────────
    running = True
    while running:

        dt = clock.tick(FPS) / 1000.0   # delta-time en segundos

        # Eventos
        for event in pygame.event.get():
            running = _handle_events(event, agent, screen, fonts, cities)
            if not running:
                break

        # Actualizar agente (avance automático)
        agent.update(dt)

        # Dibujar
        graph_renderer.draw(agent.step, agent.inicio, agent.meta)
        panel_renderer.draw(agent)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
