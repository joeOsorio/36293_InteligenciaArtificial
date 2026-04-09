# =============================================================
#  config/settings.py
#  Todas las constantes del proyecto: ventana, colores,
#  velocidad, tamaños de fuente, etc.
#  Si quieres cambiar algo visual, este es el único archivo
#  que necesitas editar.
# =============================================================

# ── Ventana ───────────────────────────────────────────────────
WINDOW_W   = 1280
WINDOW_H   = 860
PANEL_W    = 270          # ancho del panel de información (derecha)
GRAPH_W    = WINDOW_W - PANEL_W   # ancho del área del grafo
TITLE      = "BFS — Mapa de Carreteras (Baja California / Sonora / Chihuahua)"
FPS        = 60

# ── Velocidad de animación ────────────────────────────────────
SPEED_MIN  = 1            # pasos por segundo mínimo
SPEED_MAX  = 20           # pasos por segundo máximo
SPEED_INIT = 4            # velocidad inicial

# ── Nodos ─────────────────────────────────────────────────────
NODE_RADIUS       = 16
NODE_LABEL_MAXLEN = 10    # caracteres antes de truncar

# ── Colores (R, G, B) ─────────────────────────────────────────
BG            = (10,  14,  26)
GRID_COL      = (20,  28,  48)

EDGE_DEFAULT  = (45,  65,  95)
EDGE_VISITED  = (0,   180, 255)
EDGE_PATH     = (255, 200, 0)

NODE_DEFAULT  = (30,  45,  75)
NODE_BORDER   = (70,  110, 160)
NODE_VISITED  = (0,   130, 200)
NODE_FRONTIER = (0,   200, 160)
NODE_GOAL     = (255, 200, 0)
NODE_START    = (255, 100, 50)
NODE_PATH     = (255, 220, 60)
NODE_CURRENT  = (0,   130, 200)

TEXT_PRIMARY  = (200, 220, 255)
TEXT_DIM      = (80,  110, 160)
ACCENT        = (0,   200, 255)
WHITE         = (255, 255, 255)
PANEL_BG      = (14,  20,  38)

# ── Fuentes (nombre sistema, tamaño, negrita) ─────────────────
FONT_TITLE    = ("Segoe UI", 18, True)
FONT_MEDIUM   = ("Segoe UI", 14, True)
FONT_SMALL    = ("Segoe UI", 12, False)
FONT_EDGE     = ("Segoe UI", 10, False)

# ── Leyenda ───────────────────────────────────────────────────
LEGEND_ITEMS = [
    # (color,          etiqueta)
    (NODE_START,    "Origen"),
    (NODE_GOAL,     "Destino"),
    (NODE_VISITED,  "Visitado"),
    (NODE_FRONTIER, "En cola"),
    (NODE_PATH,     "Ruta BFS"),
]

# ── Ciudad por defecto al iniciar ─────────────────────────────
DEFAULT_START = "Tijuana"
DEFAULT_GOAL  = "Chihuahua"
