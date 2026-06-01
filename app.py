import streamlit as st
from database import (
    init_db,
    obtener_equipos, crear_equipo, actualizar_equipo, eliminar_equipo,
    obtener_jugadores, crear_jugador, actualizar_jugador, eliminar_jugador,
    obtener_estadios, crear_estadio, actualizar_estadio, eliminar_estadio,
)

POSICIONES = ["Base", "Escolta", "Alero", "Ala-Pívot", "Pívot"]
ALTURA_MIN = 1.50
ALTURA_MAX = 2.30

init_db()

st.set_page_config(page_title="Hoops Stats Manager", page_icon="🏀", layout="wide")
st.title("🏀 Hoops Stats Manager")
st.caption("ORT Basketball Association — Sistema de Gestión de Liga")

seccion = st.sidebar.radio(
    "Navegación",
    ["Jugadores", "Equipos", "Estadios"],
    index=0,
)

# ─────────────────────────────────────────────
# JUGADORES
# ─────────────────────────────────────────────
if seccion == "Jugadores":
    st.header("Gestión de Jugadores")

    equipos = obtener_equipos()
    equipos_dict = {e.id: e.nombre for e in equipos}

    # Filtro por equipo
    opciones_filtro = ["Todos"] + [e.nombre for e in equipos]
    filtro_equipo = st.selectbox("Filtrar por equipo", opciones_filtro)

    jugadores = obtener_jugadores()
    if filtro_equipo != "Todos":
        jugadores = [j for j in jugadores if j.equipo == filtro_equipo]

    if jugadores:
        data = []
        for j in jugadores:
            data.append({
                "ID": j.id,
                "Nombre": j.nombre_completo(),
                "Posición": j.posicion,
                "Posición ideal": j.posicion_ideal(),
                "Altura (m)": j.altura,
                "Equipo": j.equipo or "—",
            })
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No hay jugadores registrados.")

    st.divider()

    tab_alta, tab_mod, tab_baja = st.tabs(["➕ Agregar", "✏️ Modificar", "🗑️ Eliminar"])

    with tab_alta:
        st.subheader("Nuevo jugador")
        with st.form("form_alta_jugador"):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre")
            apellido = col2.text_input("Apellido")
            posicion = col1.selectbox("Posición", POSICIONES)
            altura = col2.number_input("Altura (m)", min_value=ALTURA_MIN, max_value=ALTURA_MAX, step=0.01, format="%.2f")
            equipo_sel = st.selectbox("Equipo", equipos, format_func=lambda e: e.nombre)
            submitted = st.form_submit_button("Agregar jugador")

        if submitted:
            errores = []
            if not nombre.strip():
                errores.append("El nombre no puede estar vacío.")
            if not apellido.strip():
                errores.append("El apellido no puede estar vacío.")
            if errores:
                for e in errores:
                    st.error(e)
            else:
                crear_jugador(nombre.strip(), apellido.strip(), posicion, altura, equipo_sel.id)
                st.success(f"Jugador {nombre} {apellido} agregado correctamente.")
                st.rerun()

    with tab_mod:
        st.subheader("Modificar jugador")
        jugadores_todos = obtener_jugadores()
        if not jugadores_todos:
            st.info("No hay jugadores para modificar.")
        else:
            jugador_sel = st.selectbox(
                "Seleccioná un jugador",
                jugadores_todos,
                format_func=lambda j: f"[{j.id}] {j.nombre_completo()}",
                key="mod_jugador_sel",
            )
            with st.form("form_mod_jugador"):
                col1, col2 = st.columns(2)
                nuevo_nombre = col1.text_input("Nombre", value=jugador_sel.nombre)
                nuevo_apellido = col2.text_input("Apellido", value=jugador_sel.apellido)
                nueva_posicion = col1.selectbox("Posición", POSICIONES, index=POSICIONES.index(jugador_sel.posicion) if jugador_sel.posicion in POSICIONES else 0)
                nueva_altura = col2.number_input("Altura (m)", min_value=ALTURA_MIN, max_value=ALTURA_MAX, value=float(jugador_sel.altura), step=0.01, format="%.2f")
                equipo_actual_idx = next((i for i, e in enumerate(equipos) if e.nombre == jugador_sel.equipo), 0)
                nuevo_equipo = st.selectbox("Equipo", equipos, index=equipo_actual_idx, format_func=lambda e: e.nombre, key="mod_equipo")
                guardar = st.form_submit_button("Guardar cambios")

            if guardar:
                errores = []
                if not nuevo_nombre.strip():
                    errores.append("El nombre no puede estar vacío.")
                if not nuevo_apellido.strip():
                    errores.append("El apellido no puede estar vacío.")
                if errores:
                    for e in errores:
                        st.error(e)
                else:
                    actualizar_jugador(jugador_sel.id, nuevo_nombre.strip(), nuevo_apellido.strip(), nueva_posicion, nueva_altura, nuevo_equipo.id)
                    st.success("Jugador actualizado correctamente.")
                    st.rerun()

    with tab_baja:
        st.subheader("Eliminar jugador")
        jugadores_todos = obtener_jugadores()
        if not jugadores_todos:
            st.info("No hay jugadores para eliminar.")
        else:
            jugador_del = st.selectbox(
                "Seleccioná un jugador",
                jugadores_todos,
                format_func=lambda j: f"[{j.id}] {j.nombre_completo()}",
                key="del_jugador_sel",
            )
            if st.button("Eliminar jugador", type="primary"):
                eliminar_jugador(jugador_del.id)
                st.success(f"Jugador eliminado correctamente.")
                st.rerun()

# ─────────────────────────────────────────────
# EQUIPOS
# ─────────────────────────────────────────────
elif seccion == "Equipos":
    st.header("Gestión de Equipos")

    equipos = obtener_equipos()
    if equipos:
        data = [{"ID": e.id, "Nombre": e.nombre, "Ciudad": e.ciudad, "Entrenador": e.entrenador} for e in equipos]
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No hay equipos registrados.")

    st.divider()

    tab_alta, tab_mod, tab_baja = st.tabs(["➕ Agregar", "✏️ Modificar", "🗑️ Eliminar"])

    with tab_alta:
        st.subheader("Nuevo equipo")
        with st.form("form_alta_equipo"):
            nombre = st.text_input("Nombre del equipo")
            ciudad = st.text_input("Ciudad")
            entrenador = st.text_input("Entrenador")
            submitted = st.form_submit_button("Agregar equipo")

        if submitted:
            errores = []
            if not nombre.strip():
                errores.append("El nombre no puede estar vacío.")
            if not ciudad.strip():
                errores.append("La ciudad no puede estar vacía.")
            if not entrenador.strip():
                errores.append("El entrenador no puede estar vacío.")
            if errores:
                for e in errores:
                    st.error(e)
            else:
                crear_equipo(nombre.strip(), ciudad.strip(), entrenador.strip())
                st.success(f"Equipo '{nombre}' agregado correctamente.")
                st.rerun()

    with tab_mod:
        st.subheader("Modificar equipo")
        equipos = obtener_equipos()
        if not equipos:
            st.info("No hay equipos para modificar.")
        else:
            equipo_sel = st.selectbox(
                "Seleccioná un equipo",
                equipos,
                format_func=lambda e: f"[{e.id}] {e.nombre}",
                key="mod_equipo_sel",
            )
            with st.form("form_mod_equipo"):
                nuevo_nombre = st.text_input("Nombre", value=equipo_sel.nombre)
                nueva_ciudad = st.text_input("Ciudad", value=equipo_sel.ciudad)
                nuevo_entrenador = st.text_input("Entrenador", value=equipo_sel.entrenador)
                guardar = st.form_submit_button("Guardar cambios")

            if guardar:
                errores = []
                if not nuevo_nombre.strip():
                    errores.append("El nombre no puede estar vacío.")
                if not nueva_ciudad.strip():
                    errores.append("La ciudad no puede estar vacía.")
                if not nuevo_entrenador.strip():
                    errores.append("El entrenador no puede estar vacío.")
                if errores:
                    for e in errores:
                        st.error(e)
                else:
                    actualizar_equipo(equipo_sel.id, nuevo_nombre.strip(), nueva_ciudad.strip(), nuevo_entrenador.strip())
                    st.success("Equipo actualizado correctamente.")
                    st.rerun()

    with tab_baja:
        st.subheader("Eliminar equipo")
        equipos = obtener_equipos()
        if not equipos:
            st.info("No hay equipos para eliminar.")
        else:
            equipo_del = st.selectbox(
                "Seleccioná un equipo",
                equipos,
                format_func=lambda e: f"[{e.id}] {e.nombre}",
                key="del_equipo_sel",
            )
            st.warning("⚠️ Eliminar un equipo puede afectar jugadores y estadios asociados.")
            if st.button("Eliminar equipo", type="primary"):
                eliminar_equipo(equipo_del.id)
                st.success("Equipo eliminado correctamente.")
                st.rerun()

# ─────────────────────────────────────────────
# ESTADIOS
# ─────────────────────────────────────────────
elif seccion == "Estadios":
    st.header("Gestión de Estadios")

    estadios = obtener_estadios()

    # Filtro por aptitud para final
    filtro_final = st.checkbox("Solo estadios aptos para finales (capacidad ≥ 5.000)")
    if filtro_final:
        estadios = [es for es in estadios if es.cumple_capacidad_final()]

    if estadios:
        data = []
        for es in estadios:
            data.append({
                "ID": es.id,
                "Estadio": es.nombre_estadio,
                "Capacidad": es.capacidad,
                "Equipo local": es.equipo_local or "—",
                "Apto para final": "✅" if es.cumple_capacidad_final() else "❌",
            })
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No hay estadios registrados.")

    st.divider()

    equipos = obtener_equipos()
    tab_alta, tab_mod, tab_baja = st.tabs(["➕ Agregar", "✏️ Modificar", "🗑️ Eliminar"])

    with tab_alta:
        st.subheader("Nuevo estadio")
        with st.form("form_alta_estadio"):
            nombre_estadio = st.text_input("Nombre del estadio")
            capacidad = st.number_input("Capacidad", min_value=1, step=100)
            equipo_local = st.selectbox("Equipo local", equipos, format_func=lambda e: e.nombre)
            submitted = st.form_submit_button("Agregar estadio")

        if submitted:
            if not nombre_estadio.strip():
                st.error("El nombre del estadio no puede estar vacío.")
            else:
                crear_estadio(nombre_estadio.strip(), int(capacidad), equipo_local.id)
                st.success(f"Estadio '{nombre_estadio}' agregado correctamente.")
                st.rerun()

    with tab_mod:
        st.subheader("Modificar estadio")
        estadios_todos = obtener_estadios()
        if not estadios_todos:
            st.info("No hay estadios para modificar.")
        else:
            estadio_sel = st.selectbox(
                "Seleccioná un estadio",
                estadios_todos,
                format_func=lambda es: f"[{es.id}] {es.nombre_estadio}",
                key="mod_estadio_sel",
            )
            equipo_actual_idx = next((i for i, e in enumerate(equipos) if e.nombre == estadio_sel.equipo_local), 0)
            with st.form("form_mod_estadio"):
                nuevo_nombre = st.text_input("Nombre del estadio", value=estadio_sel.nombre_estadio)
                nueva_capacidad = st.number_input("Capacidad", min_value=1, step=100, value=estadio_sel.capacidad)
                nuevo_equipo = st.selectbox("Equipo local", equipos, index=equipo_actual_idx, format_func=lambda e: e.nombre, key="mod_equipo_estadio")
                guardar = st.form_submit_button("Guardar cambios")

            if guardar:
                if not nuevo_nombre.strip():
                    st.error("El nombre del estadio no puede estar vacío.")
                else:
                    actualizar_estadio(estadio_sel.id, nuevo_nombre.strip(), int(nueva_capacidad), nuevo_equipo.id)
                    st.success("Estadio actualizado correctamente.")
                    st.rerun()

    with tab_baja:
        st.subheader("Eliminar estadio")
        estadios_todos = obtener_estadios()
        if not estadios_todos:
            st.info("No hay estadios para eliminar.")
        else:
            estadio_del = st.selectbox(
                "Seleccioná un estadio",
                estadios_todos,
                format_func=lambda es: f"[{es.id}] {es.nombre_estadio}",
                key="del_estadio_sel",
            )
            if st.button("Eliminar estadio", type="primary"):
                eliminar_estadio(estadio_del.id)
                st.success("Estadio eliminado correctamente.")
                st.rerun()
