import matplotlib.pyplot as plt
import networkx as nx

class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.factorEQ = 0
        self.padre = None
        self.der = None
        self.izq = None

class Arbol:
    def __init__(self):
        self.raiz = None

def calcular_altura(nodo):
    if nodo is None:
        return 0
    return max(calcular_altura(nodo.izq), calcular_altura(nodo.der)) + 1

def calcular_factor_equilibrio(nodo):
    return calcular_altura(nodo.der) - calcular_altura(nodo.izq)

def rotar_izquierda(a, n):
    aux = n.der
    q = aux.izq
    n.der = q
    if q:
        q.padre = n
    aux.izq = n
    p = n.padre
    n.padre = aux
    aux.padre = p
    if p is None:
        a.raiz = aux
    else:
        if n == p.izq:
            p.izq = aux
        else:
            p.der = aux
    n.factorEQ = calcular_factor_equilibrio(n)
    aux.factorEQ = calcular_factor_equilibrio(aux)

def rotar_derecha(a, n):
    aux = n.izq
    q = aux.der
    n.izq = q
    if q:
        q.padre = n
    aux.der = n
    p = n.padre
    n.padre = aux
    aux.padre = p
    if p is None:
        a.raiz = aux
    else:
        if n == p.izq:
            p.izq = aux
        else:
            p.der = aux
    n.factorEQ = calcular_factor_equilibrio(n)
    aux.factorEQ = calcular_factor_equilibrio(aux)

def rotar_doble_derecha(a, nodo):
    rotar_derecha(a, nodo.der)
    rotar_izquierda(a, nodo)

def rotar_doble_izquierda(a, nodo):
    rotar_izquierda(a, nodo.izq)
    rotar_derecha(a, nodo)

def balancear(a, p):
    if p:
        padre = p.padre
        p.factorEQ = calcular_factor_equilibrio(p)
        if p.factorEQ > 1:
            if calcular_factor_equilibrio(p.der) < 0:
                rotar_doble_izquierda(a, p)
            else:
                rotar_izquierda(a, p)
        elif p.factorEQ < -1:
            if calcular_factor_equilibrio(p.izq) > 0:
                rotar_doble_derecha(a, p)
            else:
                rotar_derecha(a, p)
        balancear(a, padre)

def insertar_nodo(a, n):
    if a.raiz is None:
        a.raiz = n
    else:
        aux = a.raiz
        while aux:
            ant = aux
            if n.dato > aux.dato:
                aux = aux.der
            else:
                aux = aux.izq
        n.padre = ant
        if n.dato > ant.dato:
            ant.der = n
        else:
            ant.izq = n
        balancear(a, ant)

def buscar(arbol, n):
    if arbol is None:
        return False
    if arbol.dato == n:
        return True
    elif n < arbol.dato:
        return buscar(arbol.izq, n)
    else:
        return buscar(arbol.der, n)

def minimo(arbol):
    while arbol.izq:
        arbol = arbol.izq
    return arbol

def reemplazar(arbol, nuevo):
    if arbol.padre:
        if arbol.dato == arbol.padre.izq.dato:
            arbol.padre.izq = nuevo
        else:
            arbol.padre.der = nuevo
    if nuevo:
        nuevo.padre = arbol.padre

def destruir_nodo(nodo):
    nodo.izq = None
    nodo.der = None

def eliminar_nodo(nodo):
    if nodo.izq and nodo.der:
        menor = minimo(nodo.der)
        nodo.dato = menor.dato
        eliminar_nodo(menor)
    elif nodo.izq:
        reemplazar(nodo, nodo.izq)
        destruir_nodo(nodo)
    elif nodo.der:
        reemplazar(nodo, nodo.der)
        destruir_nodo(nodo)
    else:
        reemplazar(nodo, None)
        destruir_nodo(nodo)

def eliminar(arbol, n):
    if arbol is None:
        return
    elif n < arbol.dato:
        eliminar(arbol.izq, n)
    elif n > arbol.dato:
        eliminar(arbol.der, n)
    else:
        eliminar_nodo(arbol)

def pre_orden(nodo, resultado):
    if nodo:
        resultado.append(nodo.dato)
        pre_orden(nodo.izq, resultado)
        pre_orden(nodo.der, resultado)

def in_orden(nodo, resultado):
    if nodo:
        in_orden(nodo.izq, resultado)
        resultado.append(nodo.dato)
        in_orden(nodo.der, resultado)

def post_orden(nodo, resultado):
    if nodo:
        post_orden(nodo.izq, resultado)
        post_orden(nodo.der, resultado)
        resultado.append(nodo.dato)

def dibujar_arbol(nodo, G, pos=None, nivel=0, distancia=2, x=0):
    if nodo is None:
        return pos
    if pos is None:
        pos = {nodo: (x, -nivel * 2)}
    else:
        pos[nodo] = (x, -nivel * 2)
    
    if nodo.izq:
        G.add_edge(nodo, nodo.izq)
        pos = dibujar_arbol(nodo.izq, G, pos, nivel + 1, distancia / 2, x - distancia)
    
    if nodo.der:
        G.add_edge(nodo, nodo.der)
        pos = dibujar_arbol(nodo.der, G, pos, nivel + 1, distancia / 2, x + distancia)
    
    return pos

def mostrar_arbol(arbol):
    G = nx.DiGraph()
    pos = dibujar_arbol(arbol.raiz, G)
    nx.draw(G, pos, with_labels=True, labels={nodo: nodo.dato for nodo in G.nodes}, node_size=5000, node_color='lightblue', font_size=10, font_weight='bold')
    plt.title("Árbol AVL")
    plt.show()

def menu():
    a = Arbol()
    while True:
        print("Menu")
        print("1. Insertar un nuevo nodo")
        print("2. Mostrar el arbol completo")
        print("3. Buscar un elemento en el arbol")
        print("4. Eliminar nodo del arbol")
        print("5. PreOrden")
        print("6. InOrden")
        print("7. PostOrden")
        print("8. Salir")
        opcion = int(input("Opcion: "))

        if opcion == 1:
            dato = int(input("Ingrese un numero: "))
            insertar_nodo(a, Nodo(dato))
        elif opcion == 2:
            print("Mostrando el arbol completo")
            mostrar_arbol(a)
        elif opcion == 3:
            dato = int(input("Digite el elemento a buscar: "))
            if buscar(a.raiz, dato):
                print("El elemento ha sido encontrado en el arbol")
            else:
                print("Elemento no encontrado")
        elif opcion == 4:
            dato = int(input("Digite el numero a eliminar: "))
            eliminar(a.raiz, dato)
        elif opcion == 5:
            resultado = []
            pre_orden(a.raiz, resultado)
            print("Recorrido en PreOrden: ", resultado)
        elif opcion == 6:
            resultado = []
            in_orden(a.raiz, resultado)
            print("Recorrido en InOrden: ", resultado)
        elif opcion == 7:
            resultado = []
            post_orden(a.raiz, resultado)
            print("Recorrido en PostOrden: ", resultado)
        elif opcion == 8:
            break
        else:
            print("Opción no válida")

if __name__ == "__main__":
    menu()
