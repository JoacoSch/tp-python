Proyecto: Sistema de Gestión "Hoops Stats Manager"
Historia
La federación de básquet "ORT Basketball Association" ha decidido dar el salto digital. Actualmente, el registro de los jugadores, los equipos de la liga y los estadios donde se disputan las fechas se lleva adelante mediante planillas impresas que se completan a mano durante los partidos, lo que genera errores en las estadísticas y pérdida de datos valiosos sobre el desempeño de los deportistas.
Te han contratado para desarrollar "Hoops Stats Manager", una aplicación centralizada para que los comisionados de la liga puedan gestionar toda la información del torneo. El objetivo es que la app permita administrar los perfiles de los jugadores, los datos de los clubes y la infraestructura de los estadios (canchas), asegurando que la información de la federación persista de manera organizada en el tiempo.
Objetivos del Proyecto
1. Arquitectura de Datos (Clases y POO)
A partir del script de base de datos provisto, el equipo deberá:
Diseñar e implementar las clases Python necesarias que representen las entidades del mundo real.
Cada clase debe tener su método __init__ y, al menos, dos métodos de instancia (por ejemplo: un método para determinar la posición ideal del jugador según su altura o un método que verifique si el estadio cumple con la capacidad mínima para una final).
Utilizar listas o diccionarios para procesar los objetos recuperados de la base de datos antes de mostrarlos en la interfaz.
2. Persistencia con SQLite
Implementar una capa de datos (funciones) que realice la conexión a la base de datos.
Desarrollar un CRUD completo (Crear, Leer, Actualizar, Borrar) que afecte a las tablas principales de la liga.
Asegurar que las operaciones de "Baja" y "Modificación" se realicen de forma segura (por ID).
3. Interfaz Gráfica (Streamlit)
La aplicación debe ser intuitiva y contar con:
Menú de Navegación: Diferenciar claramente entre la gestión de Jugadores, Equipos y Sedes (Estadios).
Visualización Dinámica: Listar los datos permitiendo el uso de filtros (por ejemplo: filtrar jugadores por equipo o estadios por tipo de superficie de madera/parquet).
Formularios de Carga: Para las altas debe haber formularios que registren los datos de manera exitosa, permitiendo asociar a un jugador con su equipo correspondiente.
4. Lógica de Programación
Condicionales: Validar que no se carguen campos vacíos o valores incoherentes (ej: altura de jugador fuera de rango lógico o capacidad de estadio menor a cero).
Repetitivas: Utilizar bucles para transformar los registros de la base de datos en objetos de las clases creadas.
Funciones: El código debe estar modularizado; no debe haber lógica de SQL mezclada directamente con el código de la interfaz de Streamlit.

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
