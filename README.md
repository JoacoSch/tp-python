# Hoops Stats Manager

Sistema de gestión para la **ORT Basketball Association** que permite administrar jugadores, equipos y estadios de la liga mediante una interfaz web interactiva.

## Tecnologías

- **Python 3** — lenguaje principal
- **Streamlit** — interfaz gráfica web
- **SQLite** — base de datos local (`liga_basquet.db`)

## Estructura del proyecto

```
tp-python/
├── app.py          # Interfaz Streamlit (punto de entrada)
├── database.py     # Capa de datos: conexión a SQLite y CRUD
├── models.py       # Clases Python: Equipo, Jugador, Estadio
├── jugadores.csv   # Dataset propio (15 jugadores) para importar
├── sqlite.py       # Script de inicialización de la base de datos
└── liga_basquet.db # Base de datos SQLite (se crea automáticamente)
```

## Cómo ejecutar

1. Instalar dependencias:
   ```bash
   pip install streamlit pandas
   ```

2. Iniciar la aplicación:
   ```bash
   streamlit run app.py
   ```

La base de datos se crea automáticamente al primer inicio si no existe.

## Funcionamiento

La app se divide en tres secciones accesibles desde el menú lateral:

### Jugadores

- Lista todos los jugadores con nombre completo, posición registrada, **posición ideal** (calculada según altura), altura y equipo.
- Filtro por equipo mediante un selector desplegable.
- Tabs para **agregar**, **modificar** y **eliminar** jugadores.
- Validaciones: nombre y apellido no pueden estar vacíos; la altura debe estar entre 1,50 m y 2,30 m.
- La posición ideal se determina automáticamente por altura:

  | Altura mínima | Posición ideal |
  |---------------|----------------|
  | 1,95 m        | Pívot          |
  | 1,88 m        | Ala-Pívot      |
  | 1,83 m        | Alero          |
  | 1,78 m        | Escolta        |
  | < 1,78 m      | Base           |

### Equipos

- Lista todos los equipos con nombre, ciudad y entrenador.
- Tabs para **agregar**, **modificar** y **eliminar** equipos.
- Validaciones: ningún campo puede estar vacío.
- Al eliminar un equipo se muestra una advertencia sobre el impacto en jugadores y estadios asociados.

### Estadios

- Lista todos los estadios con nombre, capacidad, equipo local e indicador de si es **apto para finales** (capacidad ≥ 5.000 espectadores).
- Filtro mediante checkbox para mostrar solo estadios aptos para finales.
- Tabs para **agregar**, **modificar** y **eliminar** estadios.
- Validaciones: el nombre no puede estar vacío y la capacidad debe ser mayor a cero.

### Estadísticas

- Lee los jugadores con `pandas.read_sql` y calcula **media, mediana y moda** de la altura.
- Muestra los tres valores rotulados y un párrafo que interpreta los resultados.
- Los datos se cargan con el botón **Importar jugadores desde jugadores.csv** de la sección Jugadores (usa `pandas.read_csv` y `crear_jugador` fila por fila; omite los que ya existen).

## Arquitectura

- `models.py` define las clases `Equipo`, `Jugador` y `Estadio` con métodos de instancia para lógica de negocio (posición ideal del jugador, verificación de capacidad para finales).
- `database.py` centraliza toda la lógica SQL: cada función recibe parámetros simples, ejecuta la query correspondiente y devuelve objetos de las clases del modelo.
- `app.py` solo contiene código de interfaz; no mezcla SQL con la presentación.
