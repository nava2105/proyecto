import networkx as nx
import matplotlib.pyplot as plt

def graficar_red(matriz, nodos):
    """
    Grafica la red a partir de una matriz de adyacencia.
    """
    G = nx.DiGraph()
    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if matriz[i][j] > 0:
                G.add_edge(nodos[i], nodos[j], weight=matriz[i][j])

    # Dibujar la red
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, font_weight="bold")
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    return plt

def ruta_mas_corta(matriz, nodos, origen, destino):
    """
    Encuentra la ruta más corta usando el algoritmo de Dijkstra.
    """
    G = nx.DiGraph()
    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if matriz[i][j] > 0:
                G.add_edge(nodos[i], nodos[j], weight=matriz[i][j])

    try:
        ruta = nx.dijkstra_path(G, source=origen, target=destino, weight="weight")
        costo = nx.dijkstra_path_length(G, source=origen, target=destino, weight="weight")
        pasos = [
            f"1. Inicialización: Nodo de origen = {origen}, Nodo de destino = {destino}.",
            f"2. Aplicando el algoritmo de Dijkstra...",
            f"3. Ruta más corta encontrada: {' → '.join(ruta)}.",
            f"4. Costo total de la ruta: {costo}."
        ]
        return ruta, costo, pasos
    except nx.NetworkXNoPath:
        return None, None, ["No existe una ruta entre los nodos seleccionados."]

def flujo_maximo(matriz, nodos, origen, destino):
    """
    Calcula el flujo máximo usando el algoritmo de Ford-Fulkerson.
    """
    G = nx.DiGraph()
    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if matriz[i][j] > 0:
                G.add_edge(nodos[i], nodos[j], capacity=matriz[i][j])

    try:
        flujo_valor, flujo_dict = nx.maximum_flow(G, origen, destino)
        pasos = [
            f"1. Inicialización: Nodo de origen = {origen}, Nodo de destino = {destino}.",
            f"2. Aplicando el algoritmo de Ford-Fulkerson...",
            f"3. Flujo máximo encontrado: {flujo_valor}.",
            f"4. Distribución del flujo: {flujo_dict}."
        ]
        return flujo_valor, flujo_dict, pasos
    except nx.NetworkXError as e:
        return None, None, [f"Error: {str(e)}"]

def arbol_expansion_minima(matriz, nodos):
    """
    Encuentra el árbol de expansión mínima usando el algoritmo de Kruskal.
    """
    G = nx.Graph()
    for i in range(len(nodos)):
        for j in range(len(nodos)):
            if matriz[i][j] > 0:
                G.add_edge(nodos[i], nodos[j], weight=matriz[i][j])

    if not nx.is_connected(G):
        return None, ["El grafo no es conexo. No se puede calcular el árbol de expansión mínima."]

    arbol = nx.minimum_spanning_tree(G, weight="weight")
    pasos = [
        "1. Inicialización: Creando el grafo no dirigido.",
        "2. Aplicando el algoritmo de Kruskal...",
        "3. Árbol de expansión mínima encontrado."
    ]
    return arbol, pasos

import networkx as nx

def flujo_costo_minimo(matriz, nodos, balances):
    """
    Resuelve el problema de flujo de costo mínimo y devuelve la solución.
    """
    try:
        # Crear el grafo dirigido
        G = nx.DiGraph()

        # Agregar nodos con balances de flujo
        for i, nodo in enumerate(nodos):
            G.add_node(nodo, demand=balances[i])

        # Agregar aristas con capacidades y costos
        for i in range(len(nodos)):
            for j in range(len(nodos)):
                if matriz[i][j] > 0:
                    G.add_edge(nodos[i], nodos[j], capacity=matriz[i][j], weight=matriz[i][j])

        # Resolver el problema de flujo de costo mínimo
        flujo = nx.min_cost_flow(G)

        # Calcular el costo total
        costo_total = nx.cost_of_flow(G, flujo)

        # Preparar los pasos detallados
        pasos = [
            "1. Modelo matemático del flujo de costo mínimo:",
            "   Minimizar Z = ∑(c_ij * x_ij) para todas las aristas (i,j).",
            "   Sujeto a:",
            "   - ∑x_ij - ∑x_ji = b_i para todos los nodos i.",
            "   - 0 ≤ x_ij ≤ u_ij para todas las aristas (i,j).",
            "2. Solución específica:",
            f"   Costo total mínimo: {costo_total}.",
            "   Flujos en las aristas:"
        ]

        # Mostrar los flujos en cada arista
        for u in flujo:
            for v in flujo[u]:
                if flujo[u][v] > 0:
                    pasos.append(f"   - {u} → {v}: Flujo = {flujo[u][v]}")

        return pasos

    except Exception as e:
        return [f"Error: {str(e)}"]