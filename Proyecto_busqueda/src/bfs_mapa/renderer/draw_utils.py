# =============================================================
#  renderer/draw_utils.py
#  Primitivas de dibujo reutilizables (sin lógica de dominio).
#
#  Responsabilidades:
#    - Rectángulos con bordes redondeados y transparencia
#    - Líneas con transparencia (aristas del grafo)
#    - Nodos con glow, borde y etiqueta
# =============================================================

import pygame
from config.settings import (
    NODE_RADIUS, NODE_LABEL_MAXLEN,
    NODE_DEFAULT, NODE_BORDER, NODE_VISITED, NODE_FRONTIER,
    NODE_GOAL, NODE_START, NODE_PATH, NODE_CURRENT,
    TEXT_PRIMARY, ACCENT,
)


def draw_rounded_rect(surf, color, rect, radius=8, alpha=255):
    """
    Dibuja un rectángulo con esquinas redondeadas y soporte de alfa.

    Parámetros
    ----------
    surf   : pygame.Surface  superficie destino
    color  : tuple(R,G,B)
    rect   : tuple(x, y, w, h)
    radius : int    radio de redondeo
    alpha  : int    transparencia 0-255
    """
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0, 0, rect[2], rect[3]),
                     border_radius=radius)
    surf.blit(s, (rect[0], rect[1]))


def draw_edge(surf, p1, p2, color, width=2, alpha=200):
    """
    Dibuja una línea semitransparente entre dos puntos.

    Parámetros
    ----------
    p1, p2 : tuple(x, y)  extremos de la arista
    """
    s = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    pygame.draw.line(s, (*color, alpha), p1, p2, width)
    surf.blit(s, (0, 0))


def draw_node(surf, pos, label, state, font, radius=NODE_RADIUS):
    """
    Dibuja un nodo con color según su estado BFS.

    Estados válidos
    ---------------
    "default"  "start"  "goal"  "visited"
    "frontier" "current" "path"

    Parámetros
    ----------
    surf  : pygame.Surface
    pos   : tuple(x, y)   centro del nodo
    label : str            nombre de la ciudad
    state : str            estado BFS actual
    font  : pygame.Font    fuente para la etiqueta
    """
    x, y = pos

    # ── Colores según estado ──────────────────────────────────
    STATE_STYLES = {
        "start":    (NODE_START,    (255, 150, 80), 3),
        "goal":     (NODE_GOAL,     (255, 230, 80), 3),
        "path":     (NODE_PATH,     (255, 230, 60), 2),
        "current":  (NODE_CURRENT,  ACCENT,         3),
        "frontier": (NODE_FRONTIER, (0, 230, 180),  2),
        "visited":  (NODE_VISITED,  (0, 180, 255),  1),
        "default":  (NODE_DEFAULT,  NODE_BORDER,    1),
    }
    fill, border, border_w = STATE_STYLES.get(state, STATE_STYLES["default"])

    # ── Glow para nodos destacados ────────────────────────────
    if state in ("current", "goal", "start", "path"):
        glow = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*fill, 40),
                           (radius * 2, radius * 2), radius * 2)
        surf.blit(glow, (x - radius * 2, y - radius * 2))

    # ── Círculo principal ─────────────────────────────────────
    pygame.draw.circle(surf, fill,   (x, y), radius)
    pygame.draw.circle(surf, border, (x, y), radius, border_w)

    # ── Etiqueta truncada debajo del nodo ─────────────────────
    short = (label if len(label) <= NODE_LABEL_MAXLEN
             else label[:NODE_LABEL_MAXLEN - 1] + "…")
    txt = font.render(short, True, TEXT_PRIMARY)
    surf.blit(txt, (x - txt.get_width() // 2, y + radius + 3))
