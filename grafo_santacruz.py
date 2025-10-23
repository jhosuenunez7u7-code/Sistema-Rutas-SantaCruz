# =====================================================
# PROYECTO FINAL – ESTRUCTURA DE DATOS II
# Sistema de Rutas de Santa Cruz (Grafos ponderados + Dijkstra)
# Autor: Josue Marcelo Via Núñez
# Universidad: UAGRM
# =====================================================

from typing import Dict, List, Tuple
import heapq
import unicodedata

INF = float("inf")

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================
def _norm(s: str) -> str:
    """Convierte una cadena a minúsculas y elimina acentos/tildes."""
    s = s.strip().lower()
    s = unicodedata.normalize("NFKD", s)
    return "".join(c for c in s if not unicodedata.combining(c))

# =====================================================
# CLASE GRAFO
# =====================================================
class Grafo:
    def __init__(self, vertices: List[str]):
        """Inicializa un grafo no dirigido y ponderado"""
        self.vertices = vertices
        self.adyacencia: Dict[str, List[Tuple[str, float]]] = {v: [] for v in vertices}
        self._name_by_norm = {_norm(v): v for v in self.vertices}  # índice normalizado

    # ---------- MÉTODOS PRINCIPALES ----------
    def agregar_arista(self, origen: str, destino: str, peso: float):
        """Agrega una conexión bidireccional entre dos ciudades"""
        if origen not in self.vertices or destino not in self.vertices:
            print("⚠️ Ciudad no encontrada.")
            return
        self.adyacencia[origen].append((destino, peso))
        self.adyacencia[destino].append((origen, peso))

    def mostrar_lista_adyacencia(self):
        """Muestra la lista de adyacencia"""
        print("\n📍 Lista de Adyacencia:")
        for v in self.vertices:
            conexiones = ", ".join([f"{d} ({p} km)" for d, p in self.adyacencia[v]])
            print(f"  {v} ➜ {conexiones}")
        input("\nPresiona Enter para continuar...")

    def mostrar_matriz_adyacencia(self):
        """Muestra la matriz de adyacencia"""
        print("\n🧮 Matriz de Adyacencia (Distancias en km):")
        print("     " + "  ".join(f"{v[:3]}" for v in self.vertices))
        for o in self.vertices:
            fila = []
            for d in self.vertices:
                peso = next((p for x, p in self.adyacencia[o] if x == d), 0)
                fila.append(f"{peso:>3}")
            print(f"{o[:3]}  {'  '.join(fila)}")
        input("\nPresiona Enter para continuar...")

    def dijkstra(self, inicio: str, destino: str):
        """Calcula el camino más corto usando Dijkstra"""
        distancias = {v: INF for v in self.vertices}
        anteriores = {v: None for v in self.vertices}
        distancias[inicio] = 0

        cola = [(0, inicio)]
        while cola:
            dist, actual = heapq.heappop(cola)
            if dist > distancias[actual]:
                continue
            for vecino, peso in self.adyacencia[actual]:
                nueva_dist = dist + peso
                if nueva_dist < distancias[vecino]:
                    distancias[vecino] = nueva_dist
                    anteriores[vecino] = actual
                    heapq.heappush(cola, (nueva_dist, vecino))

        camino = []
        nodo = destino
        while nodo:
            camino.insert(0, nodo)
            nodo = anteriores[nodo]
        return camino, distancias[destino]

# =====================================================
# FUNCIONES DE EJEMPLO – CIUDADES DE SANTA CRUZ
# =====================================================
def grafo_santacruz() -> Grafo:
    ciudades = [
        "Santa Cruz", "Warnes", "Montero", "Portachuelo",
        "Buena Vista", "Yapacaní", "Cotoca", "La Guardia", "El Torno"
    ]
    g = Grafo(ciudades)

    # Distancias aproximadas (km)
    g.agregar_arista("Santa Cruz", "Warnes", 27)
    g.agregar_arista("Warnes", "Montero", 17)
    g.agregar_arista("Montero", "Portachuelo", 16)
    g.agregar_arista("Portachuelo", "Buena Vista", 46)
    g.agregar_arista("Buena Vista", "Yapacaní", 50)
    g.agregar_arista("Santa Cruz", "Cotoca", 20)
    g.agregar_arista("Cotoca", "La Guardia", 28)
    g.agregar_arista("La Guardia", "El Torno", 17)
    g.agregar_arista("La Guardia", "Santa Cruz", 18)
    g.agregar_arista("Warnes", "Cotoca", 45)

    return g

# =====================================================
# MENÚ PRINCIPAL
# =====================================================
def menu():
    g = grafo_santacruz()

    while True:
        print("\n" + "="*55)
        print("   🚗 SISTEMA DE RUTAS - SANTA CRUZ (Grafos + Dijkstra)")
        print("="*55)
        print("1. Mostrar lista de adyacencia")
        print("2. Mostrar matriz de adyacencia")
        print("3. Calcular camino más corto")
        print("0. Salir")

        op = input("\nElige una opción: ")

        if op == "1":
            g.mostrar_lista_adyacencia()
        elif op == "2":
            g.mostrar_matriz_adyacencia()
        elif op == "3":
            inicio_raw = input("Ciudad de origen: ")
            destino_raw = input("Ciudad de destino: ")

            ini_key = _norm(inicio_raw)
            des_key = _norm(destino_raw)

            if ini_key in g._name_by_norm and des_key in g._name_by_norm:
                inicio = g._name_by_norm[ini_key]
                destino = g._name_by_norm[des_key]
                camino, dist = g.dijkstra(inicio, destino)
                if camino:
                    print(f"\n🗺️  Camino más corto: {' ➜ '.join(camino)}")
                    print(f"📏 Distancia total: {dist:.1f} km")
                else:
                    print("⚠️ No se pudo calcular el camino.")
            else:
                print("⚠️ Una de las ciudades no existe.")
            input("\nPresiona Enter para continuar...")
        elif op == "0":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("⚠️ Opción no válida, intenta de nuevo.")
            input("\nPresiona Enter para continuar...")

# =====================================================
if __name__ == "__main__":
    menu()
