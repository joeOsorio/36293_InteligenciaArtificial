# =============================================================
#  graph/map_data.py
#  Define el espacio de búsqueda:
#    - GRAFO : lista de adyacencia  { ciudad: [(vecino, km), …] }
#    - POSICIONES : coordenadas de pantalla { ciudad: (x, y) }
#
#  Si el mapa crece (más ciudades), solo edita este archivo.
# =============================================================

# ── Lista de adyacencia (distancias en km) ────────────────────
GRAFO = {
    # ── Baja California ──────────────────────────────────────
    "Tijuana":             [("Tecate", 52),   ("Rosarito", 20)],
    "Rosarito":            [("Tijuana", 20),  ("Ensenada", 85)],
    "Tecate":              [("Tijuana", 52),  ("Mexicali", 135), ("Ensenada", 100)],
    "Ensenada":            [("Rosarito", 85), ("Tecate", 100),
                            ("San Felipe", 246), ("San Quintin", 185)],
    "Mexicali":            [("Tecate", 135),  ("San Luis Rio Colorado", 80),
                            ("San Felipe", 197)],
    "San Felipe":          [("Mexicali", 197), ("Ensenada", 246),
                            ("Guerrero Negro", 394)],
    "San Quintin":         [("Ensenada", 185), ("Guerrero Negro", 425)],
    "Guerrero Negro":      [("San Quintin", 425), ("San Felipe", 394),
                            ("Santa Rosalia", 220)],
    "Santa Rosalia":       [("Guerrero Negro", 220), ("Mulege", 63)],
    "Mulege":              [("Santa Rosalia", 63), ("Ciudad Constitucion", 283)],
    "Ciudad Constitucion": [("Mulege", 283), ("San Carlos", 61), ("La Paz", 210)],
    "San Carlos":          [("Ciudad Constitucion", 61)],
    "La Paz":              [("Ciudad Constitucion", 210), ("San Jose del Cabo", 201),
                            ("Cabo San Lucas", 157)],
    "San Jose del Cabo":   [("La Paz", 201), ("Cabo San Lucas", 38)],
    "Cabo San Lucas":      [("San Jose del Cabo", 38), ("La Paz", 157)],

    # ── Sonora ───────────────────────────────────────────────
    "San Luis Rio Colorado": [("Mexicali", 80), ("Sonoyta", 203)],
    "Sonoyta":             [("San Luis Rio Colorado", 203), ("Puerto Penasco", 98),
                            ("Caborca", 149)],
    "Puerto Penasco":      [("Sonoyta", 98), ("Caborca", 176)],
    "Caborca":             [("Sonoyta", 149), ("Puerto Penasco", 176),
                            ("Santa Ana", 107)],
    "Santa Ana":           [("Caborca", 107), ("Nogales", 107),
                            ("Cananea", 125), ("Hermosillo", 171)],
    "Nogales":             [("Santa Ana", 107), ("Cananea", 99)],
    "Cananea":             [("Nogales", 99), ("Santa Ana", 125), ("Agua Prieta", 86)],
    "Agua Prieta":         [("Cananea", 86), ("Janos", 160), ("Moctezuma", 199)],
    "Moctezuma":           [("Agua Prieta", 199), ("Hermosillo", 178),
                            ("Yécora", 257)],
    "Yécora":              [("Moctezuma", 257), ("Hermosillo", 278),
                            ("Ciudad Cuauhtemoc", 309)],
    "Hermosillo":          [("Santa Ana", 171), ("Guaymas", 135),
                            ("Moctezuma", 178), ("Nacozari", 278)],
    "Nacozari":            [("Hermosillo", 278)],
    "Guaymas":             [("Hermosillo", 135), ("Ciudad Obregon", 130)],
    "Ciudad Obregon":      [("Guaymas", 130)],

    # ── Chihuahua ────────────────────────────────────────────
    "Janos":               [("Agua Prieta", 160), ("Ciudad Juarez", 212),
                            ("Flores Magon", 173)],
    "Ciudad Juarez":       [("Janos", 212), ("Villa Ahumada", 125)],
    "Villa Ahumada":       [("Ciudad Juarez", 125), ("Flores Magon", 93),
                            ("Sueco", 85)],
    "Flores Magon":        [("Villa Ahumada", 93), ("Sueco", 60),
                            ("Ciudad Cuauhtemoc", 211), ("Janos", 173)],
    "Sueco":               [("Flores Magon", 60), ("Villa Ahumada", 85),
                            ("Chihuahua", 158)],
    "Chihuahua":           [("Sueco", 158), ("Delicias", 87), ("Parral", 225),
                            ("Ciudad Cuauhtemoc", 105), ("Ojinaga", 379)],
    "Ojinaga":             [("Chihuahua", 379)],
    "Delicias":            [("Chihuahua", 87), ("Ciudad Jimenez", 139)],
    "Ciudad Jimenez":      [("Delicias", 139), ("Parral", 215)],
    "Parral":              [("Chihuahua", 225), ("Ciudad Jimenez", 215)],
    "Ciudad Cuauhtemoc":   [("Chihuahua", 105), ("Flores Magon", 211),
                            ("Yécora", 309)],
}

# ── Posiciones geográficas en pantalla (x, y) ─────────────────
#    Noroeste = arriba-izquierda  /  Sur = abajo
POSICIONES = {
    # Baja California
    "Tijuana":             (110, 60),
    "Rosarito":            (90,  100),
    "Tecate":              (175, 75),
    "Ensenada":            (80,  165),
    "Mexicali":            (265, 60),
    "San Felipe":          (265, 200),
    "San Quintin":         (80,  290),
    "Guerrero Negro":      (130, 400),
    "Santa Rosalia":       (165, 470),
    "Mulege":              (175, 530),
    "Ciudad Constitucion": (155, 620),
    "San Carlos":          (110, 640),
    "La Paz":              (195, 710),
    "San Jose del Cabo":   (220, 790),
    "Cabo San Lucas":      (170, 810),
    # Sonora
    "San Luis Rio Colorado": (330, 60),
    "Sonoyta":             (370, 110),
    "Puerto Penasco":      (340, 160),
    "Caborca":             (400, 185),
    "Santa Ana":           (440, 240),
    "Nogales":             (450, 310),
    "Cananea":             (510, 285),
    "Agua Prieta":         (570, 255),
    "Hermosillo":          (420, 340),
    "Nacozari":            (510, 370),
    "Moctezuma":           (555, 330),
    "Yécora":              (555, 420),
    "Guaymas":             (415, 440),
    "Ciudad Obregon":      (430, 510),
    # Chihuahua
    "Janos":               (630, 200),
    "Ciudad Juarez":       (700, 100),
    "Villa Ahumada":       (730, 160),
    "Flores Magon":        (700, 215),
    "Sueco":               (740, 270),
    "Ojinaga":             (810, 330),
    "Chihuahua":           (760, 360),
    "Ciudad Cuauhtemoc":   (680, 380),
    "Delicias":            (775, 440),
    "Ciudad Jimenez":      (790, 510),
    "Parral":              (755, 570),
}
