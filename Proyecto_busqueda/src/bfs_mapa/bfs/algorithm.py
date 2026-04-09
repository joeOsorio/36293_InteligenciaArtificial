# =============================================================
#  bfs/algorithm.py
#  Lógica pura del algoritmo BFS.
#  NO importa pygame — puede probarse de forma independiente.
#
#  Responsabilidades:
#    - Ejecutar BFS sobre cualquier grafo de adyacencia
#    - Generar la lista de "pasos" que el renderer animará
#    - Reconstruir la ruta solución
# =============================================================

from collections import deque


# ── Tipos de datos ────────────────────────────────────────────
#  Un "paso" es un snapshot del estado BFS en un momento dado.
#  El renderer lo consume para saber qué pintar.
#
#  Campos:
#    visited  : set  de nodos ya sacados de la cola
#    frontier : list de nodos actualmente en la cola FIFO
#    current  : nodo que se acaba de expandir (o None)
#    path     : lista ordenada origen→meta (vacía si no hallada)
#    found    : True si este paso es el momento del hallazgo
#    done     : True si BFS terminó (con o sin éxito)

def _make_step(visited, frontier, current=None,
               path=None, found=False, done=False):
    """Crea un diccionario-paso inmutable (copia de los contenedores)."""
    return {
        "visited":  set(visited),
        "frontier": list(frontier),
        "current":  current,
        "path":     list(path) if path else [],
        "found":    found,
        "done":     done,
    }


def _reconstruct_path(parent, goal):
    """Reconstruye el camino de origen a meta usando el mapa de padres."""
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    return path


# ── Algoritmo principal ───────────────────────────────────────

def bfs_steps(grafo, inicio, meta):
    """
    Ejecuta BFS y devuelve la lista completa de pasos para animar.

    Parámetros
    ----------
    grafo  : dict  { ciudad: [(vecino, peso), …] }
    inicio : str   nodo de inicio
    meta   : str   nodo objetivo

    Retorna
    -------
    list[dict]  Lista de pasos (ver estructura en _make_step).
    """
    steps   = []
    visited = set()
    frontier = deque()
    parent  = {}           # parent[n] = nodo del que llegamos a n

    # ── Validación ────────────────────────────────────────────
    if inicio not in grafo:
        return [_make_step(visited, frontier, done=True)]
    if meta not in grafo:
        return [_make_step(visited, frontier, done=True)]

    # ── Estado inicial ────────────────────────────────────────
    frontier.append(inicio)
    visited.add(inicio)
    parent[inicio] = None
    steps.append(_make_step(visited, frontier))

    # ── Caso borde: inicio == meta ────────────────────────────
    if inicio == meta:
        path = _reconstruct_path(parent, meta)
        steps.append(_make_step(visited, frontier,
                                current=inicio, path=path,
                                found=True, done=True))
        return steps

    # ── Bucle BFS ─────────────────────────────────────────────
    while frontier:
        node = frontier.popleft()

        # snapshot: estamos procesando 'node'
        steps.append(_make_step(visited, frontier, current=node))

        for (vecino, _peso) in grafo.get(node, []):
            if vecino not in visited:
                visited.add(vecino)
                parent[vecino] = node
                frontier.append(vecino)

                # ── Prueba temprana (early goal test) ─────────
                if vecino == meta:
                    path = _reconstruct_path(parent, meta)
                    steps.append(_make_step(visited, frontier,
                                            current=vecino, path=path,
                                            found=True, done=True))
                    return steps

        # snapshot: terminamos de expandir 'node'
        steps.append(_make_step(visited, frontier, current=node))

    # Sin solución
    steps.append(_make_step(visited, frontier, done=True))
    return steps


def get_path_cost(grafo, path):
    """
    Calcula el costo total (km) de una ruta dada.

    Parámetros
    ----------
    grafo : dict   lista de adyacencia con pesos
    path  : list   lista ordenada de nodos

    Retorna
    -------
    int  costo total, o -1 si la ruta es inválida
    """
    total = 0
    for i in range(len(path) - 1):
        origen  = path[i]
        destino = path[i + 1]
        encontrado = False
        for (vecino, costo) in grafo.get(origen, []):
            if vecino == destino:
                total += costo
                encontrado = True
                break
        if not encontrado:
            return -1
    return total
