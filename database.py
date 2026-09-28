import sqlite3
import pandas as pd
from models import Equipo, Jugador, Estadio

DB_PATH = "liga_basquet.db"
CSV_JUGADORES = "jugadores.csv"

# --- Queries ---
query_create_equipo = "INSERT INTO equipos (nombre, ciudad, entrenador) VALUES (?, ?, ?)"
query_read_all_equipos = "SELECT * FROM equipos"
query_read_one_equipo = "SELECT * FROM equipos WHERE id = ?"
query_update_equipo = "UPDATE equipos SET nombre = ?, ciudad = ?, entrenador = ? WHERE id = ?"
query_delete_equipo = "DELETE FROM equipos WHERE id = ?"

query_create_jugador = "INSERT INTO jugadores (nombre, apellido, posicion, altura, id_equipo) VALUES (?, ?, ?, ?, ?)"
query_read_all_jugadores = "SELECT * FROM jugadores"
query_read_jugadores_con_equipo = """
    SELECT j.id, j.nombre, j.apellido, j.posicion, j.altura, eq.nombre AS equipo
    FROM jugadores j
    LEFT JOIN equipos eq ON j.id_equipo = eq.id
"""
query_update_jugador = "UPDATE jugadores SET nombre = ?, apellido = ?, posicion = ?, altura = ?, id_equipo = ? WHERE id = ?"
query_delete_jugador = "DELETE FROM jugadores WHERE id = ?"

query_create_estadio = "INSERT INTO estadios (nombre_estadio, capacidad, id_equipo_local) VALUES (?, ?, ?)"
query_read_all_estadios = "SELECT * FROM estadios"
query_read_estadios_con_equipo = """
    SELECT es.id, es.nombre_estadio, es.capacidad, eq.nombre AS equipo_local
    FROM estadios es
    LEFT JOIN equipos eq ON es.id_equipo_local = eq.id
"""
query_update_estadio = "UPDATE estadios SET nombre_estadio = ?, capacidad = ?, id_equipo_local = ? WHERE id = ?"
query_delete_estadio = "DELETE FROM estadios WHERE id = ?"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    from sqlite import crear_base_basquet
    import os
    if not os.path.exists(DB_PATH):
        crear_base_basquet()


# --- CRUD Equipos ---

def crear_equipo(nombre, ciudad, entrenador):
    con = get_connection()
    con.execute(query_create_equipo, (nombre, ciudad, entrenador))
    con.commit()
    con.close()


def obtener_equipos():
    con = get_connection()
    rows = con.execute(query_read_all_equipos).fetchall()
    con.close()
    return [Equipo(r[0], r[1], r[2], r[3]) for r in rows]


def obtener_equipo(id):
    con = get_connection()
    row = con.execute(query_read_one_equipo, (id,)).fetchone()
    con.close()
    if row:
        return Equipo(row[0], row[1], row[2], row[3])
    return None


def actualizar_equipo(id, nombre, ciudad, entrenador):
    con = get_connection()
    con.execute(query_update_equipo, (nombre, ciudad, entrenador, id))
    con.commit()
    con.close()


def eliminar_equipo(id):
    con = get_connection()
    con.execute(query_delete_equipo, (id,))
    con.commit()
    con.close()


# --- CRUD Jugadores ---

def crear_jugador(nombre, apellido, posicion, altura, id_equipo):
    con = get_connection()
    con.execute(query_create_jugador, (nombre, apellido, posicion, altura, id_equipo))
    con.commit()
    con.close()


def obtener_jugadores():
    con = get_connection()
    rows = con.execute(query_read_jugadores_con_equipo).fetchall()
    con.close()
    return [Jugador(r[0], r[1], r[2], r[3], r[4], None, r[5]) for r in rows]


def actualizar_jugador(id, nombre, apellido, posicion, altura, id_equipo):
    con = get_connection()
    con.execute(query_update_jugador, (nombre, apellido, posicion, altura, id_equipo, id))
    con.commit()
    con.close()


def eliminar_jugador(id):
    con = get_connection()
    con.execute(query_delete_jugador, (id,))
    con.commit()
    con.close()


def importar_jugadores_csv(ruta=CSV_JUGADORES):
    df = pd.read_csv(ruta)
    existentes = [(j.nombre, j.apellido) for j in obtener_jugadores()]
    cargados = 0
    for _, fila in df.iterrows():
        if (fila["nombre"], fila["apellido"]) in existentes:
            continue
        crear_jugador(fila["nombre"], fila["apellido"], fila["posicion"], float(fila["altura"]), int(fila["id_equipo"]))
        cargados += 1
    return cargados


def obtener_jugadores_df():
    con = get_connection()
    df = pd.read_sql(query_read_jugadores_con_equipo, con)
    con.close()
    return df


# --- CRUD Estadios ---

def crear_estadio(nombre_estadio, capacidad, id_equipo_local):
    con = get_connection()
    con.execute(query_create_estadio, (nombre_estadio, capacidad, id_equipo_local))
    con.commit()
    con.close()


def obtener_estadios():
    con = get_connection()
    rows = con.execute(query_read_estadios_con_equipo).fetchall()
    con.close()
    return [Estadio(r[0], r[1], r[2], None, r[3]) for r in rows]


def actualizar_estadio(id, nombre_estadio, capacidad, id_equipo_local):
    con = get_connection()
    con.execute(query_update_estadio, (nombre_estadio, capacidad, id_equipo_local, id))
    con.commit()
    con.close()


def eliminar_estadio(id):
    con = get_connection()
    con.execute(query_delete_estadio, (id,))
    con.commit()
    con.close()
