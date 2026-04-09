# =============================================================
#  renderer/city_selector.py
#  Popup modal para seleccionar ciudades de origen y destino.
#
#  Responsabilidades:
#    - Mostrar overlay semitransparente
#    - Renderizar grid de botones de ciudades
#    - Manejar hover y clic del mouse
#    - Retornar la ciudad seleccionada (o None si cancela)
# =============================================================

import math
import sys
import pygame
from config.settings import (
    PANEL_BG, ACCENT, WHITE, TEXT_PRIMARY, GRID_COL,
)
from renderer.draw_utils import draw_rounded_rect


def show_city_selector(screen, cities, title, font_h, font_sm):
    """
    Muestra un popup bloqueante para que el usuario seleccione
    una ciudad de la lista.

    Parámetros
    ----------
    screen  : pygame.Surface  ventana principal
    cities  : list[str]       lista de ciudades ordenadas
    title   : str             título del popup
    font_h  : pygame.Font     fuente grande para el título
    font_sm : pygame.Font     fuente pequeña para los botones

    Retorna
    -------
    str | None   nombre de la ciudad seleccionada, o None si cancela
    """
    W, H    = screen.get_size()
    cols    = 4
    col_w   = 218
    row_h   = 30
    padding = 20

    rows  = math.ceil(len(cities) / cols)
    box_w = cols * col_w + padding * 2
    box_h = rows * row_h + 90
    bx    = (W - box_w) // 2
    by    = (H - box_h) // 2

    clock = pygame.time.Clock()

    while True:
        # ── Dibujar overlay ───────────────────────────────────
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        screen.blit(overlay, (0, 0))

        # ── Cuadro principal ──────────────────────────────────
        draw_rounded_rect(screen, PANEL_BG, (bx, by, box_w, box_h), radius=12)
        pygame.draw.rect(screen, ACCENT, (bx, by, box_w, box_h),
                         2, border_radius=12)

        # Título
        t = font_h.render(title, True, ACCENT)
        screen.blit(t, (bx + box_w // 2 - t.get_width() // 2, by + 14))

        # ── Botones ───────────────────────────────────────────
        mx_mouse, my_mouse = pygame.mouse.get_pos()
        rects = []

        for i, city in enumerate(cities):
            col = i % cols
            row = i // cols
            rx  = bx + padding + col * col_w
            ry  = by + 60 + row * row_h
            r   = pygame.Rect(rx, ry, col_w - 8, row_h - 4)
            rects.append((r, city))

            hover = r.collidepoint(mx_mouse, my_mouse)
            btn_color = (0, 120, 185) if hover else (22, 34, 58)
            draw_rounded_rect(screen, btn_color,
                              (rx, ry, col_w - 8, row_h - 4), radius=5)
            t = font_sm.render(city, True, WHITE if hover else TEXT_PRIMARY)
            screen.blit(t, (rx + 6, ry + (row_h - 4 - t.get_height()) // 2))

        # Instrucción
        hint = font_sm.render("ESC para cancelar", True, (60, 90, 130))
        screen.blit(hint, (bx + box_w // 2 - hint.get_width() // 2,
                           by + box_h - 24))

        pygame.display.flip()

        # ── Eventos ───────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    return None
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                for r, city in rects:
                    if r.collidepoint(ev.pos):
                        return city

        clock.tick(60)
