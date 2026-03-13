# visualization/renderer.py
"""
Renderer
========
Clase responsable de toda la visualización pygame.
Dibuja el laberinto, el agente, el camino y el panel de estadísticas.

Separar la visualización de la lógica permite reemplazar pygame
por otra librería sin tocar los algoritmos.
"""

import pygame
from typing import Optional, Tuple
from maze.maze import Maze
from . import colors


class Renderer:
    """Gestiona la ventana pygame y renderiza el estado del laberinto.

    Parámetros
    ----------
    maze        : Maze  – el laberinto a dibujar
    cell_size   : int   – tamaño en píxeles de cada celda (defecto 30)
    stats_width : int   – ancho del panel de estadísticas a la derecha
    fps         : int   – cuadros por segundo máximos
    """

    WALL_WIDTH = 2  # Grosor en píxeles de las paredes

    def __init__(
        self,
        maze: Maze,
        cell_size: int = 30,
        stats_width: int = 260,
        fps: int = 60,
    ):
        self.maze = maze
        self.cell_size = cell_size
        self.stats_width = stats_width
        self.fps = fps

        # Dimensiones del área del laberinto
        maze_pixel_w = maze.cols * cell_size
        maze_pixel_h = maze.rows * cell_size
        total_w = maze_pixel_w + stats_width
        total_h = max(maze_pixel_h, 420)  # Altura mínima para el panel

        pygame.init()
        self.screen = pygame.display.set_mode((total_w, total_h))
        pygame.display.set_caption("Maze AI – Visualizador de algoritmos")
        self.clock = pygame.time.Clock()

        # Fuentes
        self.font_small  = pygame.font.SysFont("monospace", 14)
        self.font_medium = pygame.font.SysFont("monospace", 17, bold=True)
        self.font_title  = pygame.font.SysFont("monospace", 20, bold=True)

    # ------------------------------------------------------------------
    # Bucle principal
    # ------------------------------------------------------------------

    def tick(self) -> bool:
        """Procesa eventos y controla FPS. Devuelve False si el usuario cierra la ventana."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        self.clock.tick(self.fps)
        return True

    # ------------------------------------------------------------------
    # Render completo
    # ------------------------------------------------------------------

    def render(
        self,
        agent_pos: Optional[Tuple[int, int]] = None,
        stats: Optional[dict] = None,
    ) -> None:
        """Dibuja un frame completo.

        Parámetros
        ----------
        agent_pos : (row, col) o None  – posición actual del agente
        stats     : dict o None        – estadísticas a mostrar en el panel
        """
        self.screen.fill(colors.BACKGROUND)
        self._draw_cells()
        self._draw_walls()
        self._draw_special_cells(agent_pos)
        self._draw_stats_panel(stats or {})
        pygame.display.flip()

    # ------------------------------------------------------------------
    # Dibujo de celdas
    # ------------------------------------------------------------------

    def _draw_cells(self) -> None:
        """Colorea el interior de cada celda según su estado."""
        cs = self.cell_size
        for row in self.maze.grid:
            for cell in row:
                x = cell.col * cs
                y = cell.row * cs
                rect = pygame.Rect(x + 1, y + 1, cs - 1, cs - 1)

                if cell.in_path:
                    color = colors.PATH
                elif cell.visited:
                    color = colors.VISITED
                else:
                    color = colors.CELL_DEFAULT

                pygame.draw.rect(self.screen, color, rect)

    def _draw_walls(self) -> None:
        """Dibuja las paredes activas de cada celda."""
        cs = self.cell_size
        w  = self.WALL_WIDTH

        for row in self.maze.grid:
            for cell in row:
                x = cell.col * cs
                y = cell.row * cs

                if cell.has_wall('N'):
                    pygame.draw.line(self.screen, colors.WALL,
                                     (x, y), (x + cs, y), w)
                if cell.has_wall('S'):
                    pygame.draw.line(self.screen, colors.WALL,
                                     (x, y + cs), (x + cs, y + cs), w)
                if cell.has_wall('W'):
                    pygame.draw.line(self.screen, colors.WALL,
                                     (x, y), (x, y + cs), w)
                if cell.has_wall('E'):
                    pygame.draw.line(self.screen, colors.WALL,
                                     (x + cs, y), (x + cs, y + cs), w)

    def _draw_special_cells(self, agent_pos: Optional[Tuple[int, int]]) -> None:
        """Dibuja inicio, meta y posición actual del agente."""
        cs = self.cell_size
        margin = cs // 6

        def filled_rect(row, col, color):
            pygame.draw.rect(
                self.screen, color,
                pygame.Rect(col * cs + margin, row * cs + margin,
                            cs - 2 * margin, cs - 2 * margin),
                border_radius=4,
            )

        # Celda de inicio
        sr, sc = self.maze.start
        filled_rect(sr, sc, colors.START)

        # Celda meta
        gr, gc = self.maze.goal
        filled_rect(gr, gc, colors.GOAL)

        # Agente (encima de cualquier otro color)
        if agent_pos:
            ar, ac = agent_pos
            filled_rect(ar, ac, colors.AGENT)

    # ------------------------------------------------------------------
    # Panel de estadísticas
    # ------------------------------------------------------------------

    def _draw_stats_panel(self, stats: dict) -> None:
        """Dibuja el panel lateral derecho con las estadísticas."""
        maze_pixel_w = self.maze.cols * self.cell_size
        panel_rect = pygame.Rect(
            maze_pixel_w, 0, self.stats_width, self.screen.get_height()
        )
        pygame.draw.rect(self.screen, colors.PANEL_BG, panel_rect)

        # Separador
        pygame.draw.line(
            self.screen, colors.WALL,
            (maze_pixel_w, 0), (maze_pixel_w, self.screen.get_height()), 2
        )

        x = maze_pixel_w + 16
        y = 20

        def draw_text(text, font, color, indent=0):
            nonlocal y
            surf = font.render(text, True, color)
            self.screen.blit(surf, (x + indent, y))
            y += surf.get_height() + 6

        # Título del panel
        draw_text("MAZE  AI", self.font_title, colors.HIGHLIGHT)
        draw_text("─" * 22, self.font_small, colors.WALL)

        # Controles
        draw_text("Controles:", self.font_medium, colors.TEXT_COLOR)
        draw_text("[ESC]  Salir", self.font_small, colors.TEXT_COLOR, 8)
        y += 10

        draw_text("─" * 22, self.font_small, colors.WALL)

        # Información del laberinto
        draw_text("Laberinto:", self.font_medium, colors.TEXT_COLOR)
        draw_text(f"Tamaño : {self.maze.rows} × {self.maze.cols}",
                  self.font_small, colors.TEXT_COLOR, 8)
        draw_text(f"Inicio : {self.maze.start}", self.font_small, colors.TEXT_COLOR, 8)
        draw_text(f"Meta   : {self.maze.goal}",  self.font_small, colors.TEXT_COLOR, 8)
        y += 10

        if stats:
            draw_text("─" * 22, self.font_small, colors.WALL)
            draw_text("Estadísticas:", self.font_medium, colors.TEXT_COLOR)

            for key, value in stats.items():
                label = f"{key:<14}: {value}"
                draw_text(label, self.font_small, colors.HIGHLIGHT, 8)

        # Leyenda de colores
        y += 20
        draw_text("─" * 22, self.font_small, colors.WALL)
        draw_text("Leyenda:", self.font_medium, colors.TEXT_COLOR)

        legend = [
            (colors.START,   "Inicio"),
            (colors.GOAL,    "Meta"),
            (colors.AGENT,   "Agente"),
            (colors.VISITED, "Visitado"),
            (colors.PATH,    "Camino"),
        ]
        for color, label in legend:
            square_rect = pygame.Rect(x, y + 2, 14, 14)
            pygame.draw.rect(self.screen, color, square_rect, border_radius=3)
            surf = self.font_small.render(label, True, colors.TEXT_COLOR)
            self.screen.blit(surf, (x + 22, y))
            y += 22

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def show_message(self, message: str, duration_ms: int = 2000) -> None:
        """Muestra un mensaje centrado en la pantalla por `duration_ms` milisegundos."""
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        text_surf = self.font_title.render(message, True, colors.HIGHLIGHT)
        cx = (self.maze.cols * self.cell_size) // 2 - text_surf.get_width() // 2
        cy = (self.maze.rows * self.cell_size) // 2 - text_surf.get_height() // 2
        self.screen.blit(text_surf, (cx, cy))
        pygame.display.flip()
        pygame.time.wait(duration_ms)

    def quit(self) -> None:
        """Cierra pygame correctamente."""
        pygame.quit()
