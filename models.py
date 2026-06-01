class Equipo:
    def __init__(self, id, nombre, ciudad, entrenador):
        self.id = id
        self.nombre = nombre
        self.ciudad = ciudad
        self.entrenador = entrenador

    def descripcion(self):
        return f"{self.nombre} ({self.ciudad}) — DT: {self.entrenador}"

    def es_de_ciudad(self, ciudad):
        return self.ciudad.lower() == ciudad.lower()


class Jugador:
    ALTURAS_POSICION = [
        (1.95, "Pívot"),
        (1.88, "Ala-Pívot"),
        (1.83, "Alero"),
        (1.78, "Escolta"),
        (0.00, "Base"),
    ]

    def __init__(self, id, nombre, apellido, posicion, altura, id_equipo, equipo=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.posicion = posicion
        self.altura = altura
        self.id_equipo = id_equipo
        self.equipo = equipo

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def posicion_ideal(self):
        for min_altura, pos in self.ALTURAS_POSICION:
            if self.altura >= min_altura:
                return pos
        return "Base"


class Estadio:
    CAPACIDAD_MINIMA_FINAL = 5000

    def __init__(self, id, nombre_estadio, capacidad, id_equipo_local, equipo_local=None):
        self.id = id
        self.nombre_estadio = nombre_estadio
        self.capacidad = capacidad
        self.id_equipo_local = id_equipo_local
        self.equipo_local = equipo_local

    def cumple_capacidad_final(self):
        return self.capacidad >= self.CAPACIDAD_MINIMA_FINAL

    def descripcion(self):
        apto = "Apto para finales" if self.cumple_capacidad_final() else "No apto para finales"
        equipo = self.equipo_local if self.equipo_local else "Sin equipo local"
        return f"{self.nombre_estadio} — Cap: {self.capacidad:,} — {equipo} — {apto}"
