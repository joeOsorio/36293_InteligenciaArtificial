# main.py
import sys
import multiprocessing
import pygame

from maze.maze import Maze
from generators import GENERATORS
from agents import AGENTS
from visualization.renderer import Renderer
from utils.stats import Stats

# ══════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════

MAZE_ROWS = 20
MAZE_COLS = 20
CELL_SIZE = 30
FPS = 30
STEPS_PER_FRAME = 1
GENERATOR_NAME = "recursive"

# Los 3 agentes que se ejecutarán en paralelo
AGENT_NAMES = ["dfs", "bfs", "right_hand"]

# ══════════════════════════════════════════════════════════════════════


def run_agent(
    agent_name: str,
    wall_data: list,
    rows: int,
    cols: int,
    start: tuple,
    goal: tuple,
    position: tuple,
):
    """Función que corre en cada proceso hijo.
    Recibe los datos del laberinto ya generado para que los 3 sean idénticos.
    """

    # Reconstruir el laberinto a partir de los datos de paredes
    maze = Maze(rows, cols)
    maze.start = start
    maze.goal = goal

    for r in range(rows):
        for c in range(cols):
            for direction, value in wall_data[r][c].items():
                maze.grid[r][c].walls[direction] = value

    # Crear agente
    agent_cls = AGENTS[agent_name]
    agent = agent_cls(maze)

    # Crear renderer — posicionamos cada ventana en un lugar diferente
    x, y = position
    import os

    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{x},{y}"

    renderer = Renderer(maze, cell_size=CELL_SIZE, fps=FPS)
    pygame.display.set_caption(f"Maze AI – {agent_name.upper()}")

    stats = Stats(
        agent_name=agent_name.upper(), generator_name=GENERATOR_NAME.capitalize()
    )
    stats.start()

    running = True
    finished = False

    while running:
        running = renderer.tick()

        if not agent.is_done():
            for _ in range(STEPS_PER_FRAME):
                agent.step()
                if agent.is_done():
                    break

        current_stats = {
            "Algoritmo": agent_name.upper(),
            "Generador": GENERATOR_NAME.capitalize(),
            "Visitados": str(agent.nodes_visited),
            "Camino": str(len(agent.get_path())) if agent.solved else "...",
            "Estado": "¡Resuelto!"
            if agent.solved
            else ("Buscando..." if not agent.is_done() else "Sin solución"),
        }

        renderer.render(agent_pos=agent.position, stats=current_stats)

        if agent.is_done() and not finished:
            finished = True
            stats.stop(
                nodes_visited=agent.nodes_visited,
                path_length=len(agent.get_path()),
                solved=agent.solved,
            )
            print(stats.summary())
            renderer.show_message(
                "¡Meta alcanzada!" if agent.solved else "Sin solución",
                duration_ms=1500,
            )

    renderer.quit()


def main():
    # 1. Generar UN solo laberinto
    maze = Maze(MAZE_ROWS, MAZE_COLS)
    generator = GENERATORS[GENERATOR_NAME]()
    generator.generate(maze)
    print(f"[OK] Laberinto {MAZE_ROWS}×{MAZE_COLS} generado con '{GENERATOR_NAME}'")

    # 2. Serializar las paredes para pasarlas a cada proceso
    wall_data = [
        [dict(maze.grid[r][c].walls) for c in range(MAZE_COLS)]
        for r in range(MAZE_ROWS)
    ]

    # 3. Posiciones de cada ventana en pantalla (x, y)
    window_width = MAZE_COLS * CELL_SIZE + 260 + 20  # ancho laberinto + panel + margen
    window_height = MAZE_ROWS * CELL_SIZE + 100  # alto laberinto + encabezado
    # positions = [
    #     (20, 50),
    #     (20 + window_width, 50),
    #     (20 + window_width * 2, 50),
    # ]
    positions = [
        (0, 50),  # DFS  – esquina superior izquierda
        (0 + window_width, 50),  # BFS  – centro
        (0, 0 + window_height),  # RIGHT HAND – abajo izquierda
    ]

    # 4. Lanzar un proceso por agente
    processes = []
    for agent_name, pos in zip(AGENT_NAMES, positions):
        p = multiprocessing.Process(
            target=run_agent,
            args=(
                agent_name,
                wall_data,
                MAZE_ROWS,
                MAZE_COLS,
                maze.start,
                maze.goal,
                pos,
            ),
        )
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("\n[OK] Todos los agentes terminaron.")


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Necesario en Windows
    main()
