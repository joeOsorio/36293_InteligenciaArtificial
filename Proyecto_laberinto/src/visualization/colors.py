# visualization/colors.py
"""
Paleta de colores para la visualización pygame.
Centralizar los colores aquí permite cambiar el tema fácilmente.
"""

# Fondo y estructura
BACKGROUND    = (18,  18,  24)   # Casi negro azulado
WALL          = (220, 220, 230)   # Blanco grisáceo para las paredes
CELL_DEFAULT  = (30,  30,  42)   # Celda no visitada

# Nodos especiales
START         = ( 50, 205,  50)   # Verde brillante
GOAL          = (255,  80,  80)   # Rojo/coral

# Estados durante la búsqueda
VISITED       = ( 60,  90, 160)   # Azul medio – celda explorada
FRONTIER      = (100, 160, 240)   # Azul claro – en la frontera/cola
PATH          = (255, 200,   0)   # Amarillo dorado – camino solución
AGENT         = (255, 120,   0)   # Naranja – posición actual del agente

# UI
TEXT_COLOR    = (220, 220, 220)
PANEL_BG      = ( 20,  20,  30)
HIGHLIGHT     = ( 80, 200, 200)   # Cian para estadísticas destacadas
