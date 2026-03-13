# Maze AI – Visualizador de Algoritmos de Búsqueda

Proyecto educativo para explorar algoritmos de generación y resolución de laberintos
con visualización en tiempo real usando Python + pygame.

## Estructura del proyecto

```
maze_ai/
├── main.py                        ← Punto de entrada
├── maze/
│   ├── cell.py                    ← Clase Cell (celdas con paredes)
│   └── maze.py                    ← Clase Maze (cuadrícula + métodos)
├── generators/
│   ├── recursive_backtracker.py   ← DFS con retroceso
│   ├── prim.py                    ← Algoritmo de Prim aleatorizado
│   └── wilson.py                  ← Caminata aleatoria sin bucles
├── agents/
│   ├── agent.py                   ← Clase base abstracta
│   ├── dfs_agent.py               ← Búsqueda en profundidad
│   ├── bfs_agent.py               ← Búsqueda en anchura (camino óptimo)
│   └── right_hand_agent.py        ← Regla de la mano derecha
├── visualization/
│   ├── renderer.py                ← Toda la lógica pygame
│   └── colors.py                  ← Paleta de colores centralizada
└── utils/
    └── stats.py                   ← Métricas de rendimiento
```

## Instalación

```bash
pip install pygame numpy
```

## Ejecución

```bash
python main.py
```

## Configuración rápida

Edita las constantes al inicio de `main.py`:

| Constante         | Descripción                          | Opciones                              |
|-------------------|--------------------------------------|---------------------------------------|
| `MAZE_ROWS`       | Filas del laberinto                  | Entero positivo                       |
| `MAZE_COLS`       | Columnas del laberinto               | Entero positivo                       |
| `CELL_SIZE`       | Píxeles por celda                    | 20–50 recomendado                     |
| `FPS`             | Velocidad de animación               | 10–60                                 |
| `STEPS_PER_FRAME` | Pasos del algoritmo por fotograma    | 1 = lento y educativo, 10 = rápido    |
| `GENERATOR_NAME`  | Algoritmo de generación              | `'recursive'`, `'prim'`, `'wilson'`  |
| `AGENT_NAME`      | Algoritmo de resolución              | `'dfs'`, `'bfs'`, `'right_hand'`     |

## Controles

| Tecla   | Acción      |
|---------|-------------|
| `ESC`   | Salir       |

## Leyenda de colores

| Color      | Significado               |
|------------|---------------------------|
| Verde      | Celda de inicio           |
| Rojo       | Celda meta                |
| Naranja    | Posición actual del agente|
| Azul       | Celda visitada            |
| Amarillo   | Camino solución           |
