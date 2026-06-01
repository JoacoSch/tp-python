import sqlite3

def crear_base_basquet():
    # Conexión (si no existe, se crea el archivo)
    conexion = sqlite3.connect('liga_basquet.db')
    cursor = conexion.cursor()

    # 1. Tabla de EQUIPOS
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ciudad TEXT,
            entrenador TEXT
        )
    ''')

    # 2. Tabla de JUGADORES (Relacionada con Equipos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            posicion TEXT, -- Base, Escolta, Alero, Ala-Pívot, Pívot
            altura REAL, -- En metros
            id_equipo INTEGER,
            FOREIGN KEY (id_equipo) REFERENCES equipos (id)
        )
    ''')

    # 3. Tabla de ESTADIOS (Relacionada con Equipos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estadios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_estadio TEXT NOT NULL,
            capacidad INTEGER,
            id_equipo_local INTEGER,
            FOREIGN KEY (id_equipo_local) REFERENCES equipos (id)
        )
    ''')

    # Datos de ejemplo iniciales
    equipos_iniciales = [
        ('Titanes de Python', 'CABA', 'Coach García'),
        ('Streamlit Bulls', 'Rosario', 'Coach Martínez'),
        ('SQLite Warriors', 'Córdoba', 'Coach Fernández')
    ]
    
    cursor.executemany('INSERT INTO equipos (nombre, ciudad, entrenador) VALUES (?, ?, ?)', equipos_iniciales)

    # Jugador de ejemplo vinculado al primer equipo
    cursor.execute('INSERT INTO jugadores (nombre, apellido, posicion, altura, id_equipo) VALUES (?, ?, ?, ?, ?)', 
                   ('Facundo', 'Campazzo', 'Base', 1.78, 1))

    conexion.commit()
    conexion.close()
    print("Base de datos 'liga_basquet.db' creada exitosamente.")

