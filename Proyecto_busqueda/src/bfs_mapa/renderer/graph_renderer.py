# =============================================================
#  renderer/graph_renderer.py
#  Renderiza el grafo de ciudades en el área izquierda.
#
#  Responsabilidades:
#    - Dibujar fondo con grid
#    - Dibujar todas las aristas (con distancia en km)
#    - Dibujar todos los nodos coloreados según estado BFS
#    - Dibujar la leyenda de colores
# =============================================================

import pygame
from config.settings import (
    BG, GRID_COL, EDGE_DEFAULT, EDGE_VISITED, EDGE_PATH,
    NODE_START, NODE_GOAL, NODE_VISITED, NODE_FRONTIER, NODE_PATH,
    TEXT_DIM, PANEL_BG, LEGEND_ITEMS, GRAPH_W,
)
from renderer.draw_utils import draw_edge, draw_node, draw_rounded_rect


class GraphRenderer:
    """
    Dibuja el grafo completo en cada frame.

    Uso
    ---
    renderer = GraphRenderer(screen, posiciones, grafo, fonts)
    renderer.draw(step)          # llamar una vez por frame
    """

    def __init__(self, screen, posiciones, grafo, fonts):
        """
        Parámetros
        ----------
        screen     : pygame.Surface  ventana principal
        posiciones : dict { ciudad: (x, y) }
        grafo      : dict lista de adyacencia
        fonts      : dict { 'sm': Font, 'edge': Font }
        """
        self._screen     = screen
        self._posiciones = posiciones
        self._grafo      = grafo
        self._font_sm    = fonts["sm"]
        self._font_edge  = fonts["edge"]
        self._W, self._H = screen.get_size()

    # ── API pública ───────────────────────────────────────────

    def draw(self, step, inicio, meta):
        """
        Dibuja fondo, aristas, nodos y leyenda para un paso BFS.

        Parámetros
        ----------
        step   : dict  snapshot BFS actual (de bfs_agent.step)
        inicio : str   ciudad de origen
        meta   : str   ciudad destino
        """
        self._draw_background()
        self._draw_edges(step)
        self._draw_nodes(step, inicio, meta)
        self._draw_legend()

    # ── Métodos privados ──────────────────────────────────────

    def _draw_background(self):
        self._screen.fill(BG)
        for gx in range(0, GRAPH_W, 40):
            pygame.draw.line(self._screen, GRID_COL,
                             (gx, 0), (gx, self._H))
        for gy in range(0, self._H, 40):
            pygame.draw.line(self._screen, GRID_COL,
                             (0, gy), (GRAPH_W, gy))

    def _draw_edges(self, step):
        """Dibuja aristas distinguiendo: ruta / visitadas / default."""
        drawn = set()

        # Aristas que forman la ruta solución
        path_edges = set()
        path = step.get("path", [])
        for i in range(len(path) - 1):
            key = tuple(sorted((path[i], path[i + 1])))
            path_edges.add(key)

        for ciudad, vecinos in self._grafo.items():
            if ciudad not in self._posiciones:
                continue
            for (vcn, dist) in vecinos:
                if vcn not in self._posiciones:
                    continue
                key = tuple(sorted((ciudad, vcn)))
                if key in drawn:
                    continue
                drawn.add(key)

                p1 = self._posiciones[ciudad]
                p2 = self._posiciones[vcn]

                if key in path_edges:
                    col, w, a = EDGE_PATH, 4, 240
                elif (ciudad in step["visited"]
                      and vcn in step["visited"]):
                    col, w, a = EDGE_VISITED, 2, 160
                else:
                    col, w, a = EDGE_DEFAULT, 1, 120

                draw_edge(self._screen, p1, p2, col, w, a)

                # Distancia sobre la arista
                mx = (p1[0] + p2[0]) // 2
                my = (p1[1] + p2[1]) // 2
                t  = self._font_edge.render(str(dist), True, TEXT_DIM)
                self._screen.blit(t, (mx - t.get_width() // 2,
                                      my - t.get_height() // 2))

    def _draw_nodes(self, step, inicio, meta):
        """Colorea cada nodo según su rol en el paso BFS actual."""
        visited  = step["visited"]
        frontier = step["frontier"]
        path     = step.get("path", [])
        current  = step.get("current")

        for ciudad, pos in self._posiciones.items():
            if ciudad == inicio and ciudad == meta:
                state = "goal"
            elif ciudad == inicio:
                state = "start"
            elif ciudad == meta:
                state = "goal"
            elif path and ciudad in path:
                state = "path"
            elif ciudad == current:
                state = "current"
            elif ciudad in frontier:
                state = "frontier"
            elif ciudad in visited:
                state = "visited"
            else:
                state = "default"

            draw_node(self._screen, pos, ciudad, state, self._font_sm)

    def _draw_legend(self):
        """Dibuja la leyenda de colores en la esquina inferior izquierda."""
        item_h = 20
        margin = 10
        items  = LEGEND_ITEMS
        lx = margin
        ly = self._H - margin - len(items) * item_h

        draw_rounded_rect(
            self._screen, PANEL_BG,
            (lx - 4, ly - 6, 118, len(items) * item_h + 10),
            radius=6, alpha=200
        )
        for color, label in items:
            pygame.draw.circle(self._screen, color, (lx + 7, ly + 7), 6)
            t = self._font_sm.render(label, True, TEXT_DIM)
            self._screen.blit(t, (lx + 18, ly))
            ly += item_h
