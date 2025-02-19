import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from programacion_lineal import simplex_paso_a_paso
from transporte_vogel import transporte_vogel
from inventario import inventario_programacion_dinamica
from redes import graficar_red, ruta_mas_corta, flujo_maximo, arbol_expansion_minima, flujo_costo_minimo

st.set_page_config(page_title="Optimización Empresarial", layout="wide")

st.title("📊 Sistema de Optimización Empresarial")

opcion = st.sidebar.selectbox(
    "Selecciona un módulo",
    ["Inicio", "Programación Lineal", "Problema de Transporte", "Redes", "Inventario"]
)

# 🔹 Inicio
if opcion == "Inicio":
    st.write("""
    ## 📌 Bienvenido al Sistema de Optimización Empresarial
    Esta herramienta te ayudará a resolver problemas con:
    - **Programación Lineal** (Optimización de producción mediante el Método Simplex).
    - **Problema de Transporte** (Método de Vogel).
    - **Redes** (Ruta más corta, Flujo máximo, Árbol de expansión mínima y Flujo de costo mínimo).
    - **Inventario** (Gestión de inventario con Programación Dinámica).
    
    Selecciona "Programación Lineal" en el menú lateral para comenzar.
    """)

# 🔹 Programación Lineal con Método Simplex
elif opcion == "Programación Lineal":
    st.header("🔹 Optimización de Producción (Método Simplex)")

    # Entrada de datos
    objetivo = st.text_input("Coeficientes de la función objetivo (separados por comas)", "3,5")
    restricciones = st.text_area("Restricciones (cada línea una ecuación, separados por comas)", "1,1,10\n2,3,20")

    if st.button("Ejecutar Método Simplex"):
        try:
            coef_objetivo = list(map(float, objetivo.split(",")))
            restricciones_lista = [list(map(float, r.split(","))) for r in restricciones.strip().split("\n")]

            # 🔹 Validar que cada restricción tiene el mismo número de coeficientes
            num_variables = len(coef_objetivo)
            for r in restricciones_lista:
                if len(r) != num_variables + 1:
                    raise ValueError("Cada restricción debe tener un número de coeficientes igual a la cantidad de variables más uno (para el recurso disponible).")

            # 🔹 Separar matriz de coeficientes (A) y valores de recursos (b)
            A = [r[:-1] for r in restricciones_lista]  # Coeficientes de las restricciones
            b = [r[-1] for r in restricciones_lista]  # Valores de los recursos disponibles

            # 🔹 Ejecutar el método Simplex
            resultado = simplex_paso_a_paso(coef_objetivo, A, b)

            # 🔹 Mostrar pasos detallados
            if "pasos_detallados" in resultado:
                st.subheader("📝 Pasos detallados del método Simplex")
                for paso in resultado["pasos_detallados"]:
                    st.write(paso)

            # 🔹 Mostrar solución óptima
            st.subheader("✅ Solución Óptima")
            st.json(resultado)

        except Exception as e:
            st.error(f"⚠ Error en el procesamiento de los datos: {e}")

# 🔹 Problema de Transporte con Método de Vogel
if opcion == "Problema de Transporte":
    st.header("🔹 Problema de Transporte (Método de Vogel)")

    # Entrada de datos
    st.subheader("Matriz de Costos")
    filas = st.number_input("Número de orígenes (filas)", min_value=1, value=2)
    columnas = st.number_input("Número de destinos (columnas)", min_value=1, value=2)

    costos = []
    for i in range(filas):
        fila = st.text_input(f"Costos para el origen {i+1} (separados por comas)", "10,20")
        costos.append(list(map(float, fila.split(","))))

    st.subheader("Oferta y Demanda")
    oferta = st.text_input("Oferta de cada origen (separados por comas)", "100,150")
    demanda = st.text_input("Demanda de cada destino (separados por comas)", "120,130")

    oferta = list(map(float, oferta.split(",")))
    demanda = list(map(float, demanda.split(",")))

    if st.button("Resolver Problema de Transporte"):
        try:
            # Validar que la oferta total sea igual a la demanda total
            if sum(oferta) != sum(demanda):
                st.error("La oferta total debe ser igual a la demanda total.")
            else:
                # Ejecutar el método de Vogel
                resultado = transporte_vogel(costos, oferta, demanda)

                # Mostrar pasos detallados
                if "pasos_detallados" in resultado:
                    st.subheader("📝 Pasos detallados del Método de Vogel")
                    for paso in resultado["pasos_detallados"]:
                        st.markdown(paso)

                # Mostrar solución final
                st.subheader("✅ Solución Final")
                st.write("Matriz de asignaciones:")
                st.dataframe(pd.DataFrame(resultado["asignaciones"]))
                st.write(f"Costo total: {resultado['costo_total']}")

        except Exception as e:
            st.error(f"⚠ Error en el procesamiento de los datos: {e}")

# 🔹 Módulo de Redes
# 🔹 Módulo de Redes
elif opcion == "Redes":
    st.header("🔹 Optimización de Redes")

    # Selección del problema de redes
    problema_redes = st.selectbox(
        "Selecciona un problema de redes",
        ["Ruta más corta", "Flujo máximo", "Árbol de expansión mínima", "Flujo de costo mínimo"]
    )

    # Entrada de datos generales para redes
    st.subheader("Ingresa los datos de la red")
    num_nodos = st.number_input("Número de nodos", min_value=2, value=4)
    nodos = [f"N{i+1}" for i in range(num_nodos)]

    # Matriz de adyacencia para costos o capacidades
    st.write("Ingresa la matriz de adyacencia (costos o capacidades):")
    matriz = []
    for i in range(num_nodos):
        fila = st.text_input(f"Conexiones desde {nodos[i]} (separadas por comas)", "0" * num_nodos)
        matriz.append(list(map(float, fila.split(","))))

    # Graficar la red y guardar la imagen inicial
    G = nx.DiGraph()
    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if matriz[i][j] > 0:
                G.add_edge(nodos[i], nodos[j], weight=matriz[i][j])

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, font_weight="bold")
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.savefig("red_inicial.png")

    st.subheader("Gráfico de la Red")
    st.image("red_inicial.png")

    if problema_redes in ["Ruta más corta", "Flujo máximo"]:
        origen = st.selectbox("Nodo de origen", nodos)
        destino = st.selectbox("Nodo de destino", nodos)

    if st.button(f"Resolver {problema_redes}"):
        if problema_redes == "Ruta más corta":
            try:
                ruta, costo, pasos = ruta_mas_corta(matriz, nodos, origen, destino)
                if ruta:
                    st.subheader("📝 Ruta más corta")
                    for paso in pasos:
                        st.write(paso)
                    st.write(f"Ruta: {' → '.join(ruta)}")
                    st.write(f"Costo total: {costo}")

                    # Graficar la ruta más corta
                    edges_ruta_corta = list(zip(ruta[:-1], ruta[1:]))
                    plt.figure(figsize=(8, 6))
                    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, font_weight="bold")
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
                    nx.draw_networkx_edges(G, pos, edgelist=edges_ruta_corta, edge_color="red", width=2)
                    plt.savefig("ruta_resaltada.png")
                    st.subheader("🔴 Ruta más corta resaltada")
                    st.image("ruta_resaltada.png")
            except nx.NetworkXNoPath:
                st.error("No se pudo encontrar una ruta más corta.")

        elif problema_redes == "Flujo máximo":
            flujo_valor, flujo_dict, pasos = flujo_maximo(matriz, nodos, origen, destino)
            if flujo_valor:
                st.subheader("📝 Flujo máximo")
                for paso in pasos:
                    st.write(paso)
        elif problema_redes == "Árbol de expansión mínima":
            arbol, pasos = arbol_expansion_minima(matriz, nodos)
            if arbol:
                st.subheader("📝 Árbol de expansión mínima")
                for paso in pasos:
                    st.write(paso)
                st.write("Aristas del árbol:")
                for arista in arbol.edges(data=True):
                    st.write(f"{arista[0]} → {arista[1]} (Peso: {arista[2]['weight']})")
        elif problema_redes == "Flujo de costo mínimo":
            st.subheader("Ingresa los balances de flujo (separados por comas)")
            balances_input = st.text_input("Balances de flujo (ejemplo: -10,0,0,10)", "-10,0,0,10")
            balances = list(map(int, balances_input.split(",")))

            # Verificar que la suma de los balances sea 0
            if sum(balances) != 0:
                st.error("La suma de los balances de flujo debe ser 0.")
            else:
                pasos = flujo_costo_minimo(matriz, nodos, balances)
                st.subheader("📝 Modelo matemático y solución del flujo de costo mínimo")
                for paso in pasos:
                   st.write(paso)

elif opcion == "Inventario":
    st.header("🔹 Gestión de Inventario (Programación Dinámica)")

    # Entrada de datos
    st.subheader("Ingresa los datos del problema de inventario")
    demanda = st.text_input("Demanda semanal (separada por comas)", "30,40,50,60")
    demanda = list(map(int, demanda.split(",")))
    costo_pedido = st.number_input("Costo de pedido", min_value=0, value=50)
    costo_almacenamiento = st.number_input("Costo de almacenamiento por unidad por semana", min_value=0, value=2)
    capacidad_maxima = st.number_input("Capacidad máxima de almacenamiento", min_value=1, value=200)
    inventario_inicial = st.number_input("Inventario inicial", min_value=0, value=50)

    if st.button("Resolver Problema de Inventario"):
        try:
            pasos = inventario_programacion_dinamica(demanda, costo_pedido, costo_almacenamiento, capacidad_maxima, inventario_inicial)
            st.subheader("📝 Solución del Problema de Inventario")
            for paso in pasos:
                st.write(paso)
        except Exception as e:
            st.error(f"⚠ Error en el procesamiento de los datos: {e}")