# =============================================================
#  renderer/panel_renderer.py
#  Renderiza el panel de información lateral (derecha).
#
#  Responsabilidades:
#    - Título y barra de progreso
#    - Origen / Destino
#    - Estado BFS (explorando, encontrado, sin ruta)
#    - Cola (frontera) y contador de visitados
#    - Ruta solución con costo en km
#    - Guía de controles
# =============================================================

import pygame
from config.settings import (
    PANEL_BG, ACCENT, GRID_COL, TEXT_PRIMARY, TEXT_DIM,
    NODE_START, NODE_GOAL, NODE_PATH, NODE_FRONTIER,
    WHITE, GRAPH_W,
)
from renderer.draw_utils import draw_rounded_rect


class PanelRenderer:
    """
    Dibuja el panel lateral de información.

    Uso
    ---
    panel = PanelRenderer(screen, fonts)
    panel.draw(agent)     # llamar una vez por frame
    """

    # Guía de controles (tecla, descripción)
    _CONTROLS = [
        ("SPACE",  "Play / Pausa"),
        ("←  →",   "Paso a paso"),
        ("R",       "Reiniciar"),
        ("↑  ↓",   "Velocidad"),
        ("TAB",     "Cambiar ciudades"),
        ("ESC",     "Salir"),
    ]

    def __init__(self, screen, fonts):
        """
        Parámetros
        ----------
        screen : pygame.Surface  ventana principal
        fonts  : dict { 'h': Font, 'md': Font, 'sm': Font }
        """
        self._screen  = screen
        self._font_h  = fonts["h"]
        self._font_md = fonts["md"]
        self._font_sm = fonts["sm"]
        self._W, self._H = screen.get_size()
        self._panel_x    = GRAPH_W

    # ── API pública ───────────────────────────────────────────

    def draw(self, agent):
        """
        Dibuja todo el panel a partir del estado del agente.

        Parámetros
        ----------
        agent : BFSAgent  instancia del agente con el paso actual
        """
        self._draw_background()
        mx = self._panel_x + 18
        y  = 20

        y = self._draw_title(mx, y)
        y = self._draw_progress(mx, y, agent)
        y = self._draw_cities(mx, y, agent)
        y = self._draw_status(mx, y, agent)
        y = self._draw_frontier(mx, y, agent)
        y = self._draw_path(mx, y, agent)
        self._draw_controls()

    # ── Secciones privadas ────────────────────────────────────

    def _draw_background(self):
        pw = self._W - self._panel_x
        draw_rounded_rect(self._screen, PANEL_BG,
                          (self._panel_x, 0, pw, self._H), radius=0)
        pygame.draw.line(self._screen, ACCENT,
                         (self._panel_x, 0), (self._panel_x, self._H), 1)

    def _draw_title(self, mx, y):
        for line in ("BFS — Búsqueda", "en Anchura"):
            t = self._font_h.render(line, True, ACCENT)
            self._screen.blit(t, (mx, y))
            y += t.get_height() + 2
        return y + 12

    def _draw_progress(self, mx, y, agent):
        pct   = agent.step_index / max(agent.total_steps - 1, 1)
        bar_w = self._W - self._panel_x - 36
        pygame.draw.rect(self._screen, GRID_COL,
                         (mx, y, bar_w, 8), border_radius=4)
        pygame.draw.rect(self._screen, ACCENT,
                         (mx, y, int(bar_w * pct), 8), border_radius=4)
        y += 14
        t = self._font_sm.render(
            f"Paso {agent.step_index + 1} / {agent.total_steps}  "
            f"({agent.speed} p/s)", True, TEXT_DIM)
        self._screen.blit(t, (mx, y))
        return y + t.get_height() + 16

    def _draw_cities(self, mx, y, agent):
        def kv(key, val, col):
            nonlocal y
            tk = self._font_sm.render(key + ": ", True, TEXT_DIM)
            tv = self._font_sm.render(val,         True, col)
            self._screen.blit(tk, (mx, y))
            self._screen.blit(tv, (mx + tk.get_width(), y))
            y += tk.get_height() + 4

        kv("Origen",  agent.inicio, NODE_START)
        kv("Destino", agent.meta,   NODE_GOAL)
        return y + 6

    def _draw_status(self, mx, y, agent):
        step = agent.step
        if not step["done"]:
            label = "🔍 Explorando..."
            col   = ACCENT
        elif step["found"]:
            label = "✅ ¡Ruta encontrada!"
            col   = NODE_GOAL
        else:
            label = "❌ Sin ruta posible"
            col   = (200, 80, 80)

        t = self._font_md.render(label, True, col)
        self._screen.blit(t, (mx, y))
        y += t.get_height() + 10

        cur  = step.get("current") or "—"
        tk   = self._font_sm.render("Nodo actual: ", True, TEXT_DIM)
        tv   = self._font_sm.render(cur,             True, ACCENT)
        self._screen.blit(tk, (mx, y))
        self._screen.blit(tv, (mx + tk.get_width(), y))
        return y + tk.get_height() + 12

    def _draw_frontier(self, mx, y, agent):
        step  = agent.step
        fron  = step["frontier"]
        label = f"Cola (frontera): {len(fron)} nodos"
        t = self._font_sm.render(label, True, TEXT_DIM)
        self._screen.blit(t, (mx, y))
        y += t.get_height() + 3

        preview = ", ".join(f[:8] for f in fron[:5])
        if len(fron) > 5:
            preview += "…"
        t = self._font_sm.render(preview or "vacía", True, NODE_FRONTIER)
        self._screen.blit(t, (mx + 10, y))
        y += t.get_height() + 8

        t = self._font_sm.render(
            f"Visitados: {len(step['visited'])}", True, TEXT_DIM)
        self._screen.blit(t, (mx, y))
        return y + t.get_height() + 16

    def _draw_path(self, mx, y, agent):
        step = agent.step
        if not step.get("path"):
            return y

        t = self._font_md.render("Ruta encontrada:", True, NODE_GOAL)
        self._screen.blit(t, (mx, y))
        y += t.get_height() + 6

        for i, node in enumerate(step["path"]):
            if y > self._H - 100:
                break
            arrow = "→ " if i > 0 else "   "
            t = self._font_sm.render(arrow + node, True, NODE_PATH)
            self._screen.blit(t, (mx + 6, y))
            y += t.get_height() + 2

        y += 6
        hops = len(step["path"]) - 1
        cost = agent.path_cost
        t = self._font_sm.render(
            f"Saltos: {hops}   |   Distancia: {cost} km", True, TEXT_DIM)
        self._screen.blit(t, (mx, y))
        return y + t.get_height() + 10

    def _draw_controls(self):
        cy = self._H - 16 - len(self._CONTROLS) * 17
        pygame.draw.line(self._screen, GRID_COL,
                         (self._panel_x, cy - 8), (self._W, cy - 8), 1)
        for key, desc in self._CONTROLS:
            tk = self._font_sm.render(key,        True, ACCENT)
            td = self._font_sm.render("  " + desc, True, TEXT_DIM)
            mx = self._panel_x + 18
            self._screen.blit(tk, (mx, cy))
            self._screen.blit(td, (mx + tk.get_width(), cy))
            cy += tk.get_height() + 3
