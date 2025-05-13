import csv
from main import tokens_list 

class Node:
    def __init__(self, nombre, token=None):
        self.nombre = nombre
        self.token = token  
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def imprimir(self, nivel=0):
        sangria = '  ' * nivel
        if self.token and 'lexeme' in self.token:
            print(f"{sangria}{self.nombre} → '{self.token['lexeme']}'")
        else:
            print(f"{sangria}{self.nombre}")
        for hijo in self.hijos:
            hijo.imprimir(nivel + 1)

def cargar_tabla_ll1(ruta_csv):
    with open(ruta_csv, newline='') as archivo:
        lector = csv.reader(archivo)
        encabezados = next(lector)[1:]
        tabla = {}
        for fila in lector:
            no_terminal = fila[0]
            producciones = [celda.strip() for celda in fila[1:]]
            tabla[no_terminal] = {}
            for terminal, produccion in zip(encabezados, producciones):
                if produccion:
                    if produccion.startswith(f"{no_terminal} ->"):
                        produccion = produccion.replace(f"{no_terminal} ->", "").strip()
                    simbolos = produccion.split()
                else:
                    simbolos = []
                tabla[no_terminal][terminal] = simbolos
        return tabla

def parse_ll1(tokens, tabla_ll1):
    stack = ['$', 'FUNCIONES']
    index = 0
    nodo_raiz = Node('FUNCIONES')
    node_stack = [Node('$'), nodo_raiz]

    while stack:
        if index >= len(tokens):
            return " Error: entrada terminada inesperadamente", None

        top = stack.pop()
        nodo_actual = node_stack.pop()
        current_token = tokens[index]['type']
        linea = tokens[index]['line']
        columna = tokens[index]['column']

        if top in tabla_ll1:
            produccion = tabla_ll1[top].get(current_token, [])
            if not produccion:
                return f" Error en token '{current_token}' (línea: {linea}, columna: {columna}): sin producción para [{top}, {current_token}]", None
            if produccion == ['e'] or produccion == ['ε']:
                nodo_actual.agregar_hijo(Node('ε'))
                continue

            hijos = []
            for simbolo in produccion:
                hijo = Node(simbolo)
                hijos.append(hijo)
                nodo_actual.agregar_hijo(hijo)
            for simbolo, nodo in zip(reversed(produccion), reversed(hijos)):
                stack.append(simbolo)
                node_stack.append(nodo)

        elif top == current_token:
            nodo_actual.token = tokens[index]
            index += 1
        elif top == 'ε':
            nodo_actual.agregar_hijo(Node('ε'))
        else:
            return f" Error en token '{current_token}' (línea: {linea}, columna: {columna}): se esperaba '{top}'", None

    if tokens[index - 1]['type'] == '$':
        return "Cadena aceptada", nodo_raiz
    else:
        return f" Error: tokens restantes sin analizar desde '{tokens[index]['type']}'", None

def generar_dot(node, dot_lines=None, parent_id=None, counter=[0]):
    if dot_lines is None:
        dot_lines = ["digraph G {", "  rankdir=TB;", "  node [style=filled, fontname=Helvetica];"]

    current_id = f'node{counter[0]}'
    counter[0] += 1

    if node.token:
        # Terminal
        label = f"{node.nombre}\\n'{node.token['lexeme']}'\\n[{node.token['line']},{node.token['column']}]"
        dot_lines.append(f'{current_id} [label="{label}", shape=ellipse, fillcolor=deepskyblue];')
    else:
        # No terminal
        dot_lines.append(f'{current_id} [label="{node.nombre}", shape=box, fillcolor=lightgreen];')

    if parent_id:
        dot_lines.append(f'{parent_id} -> {current_id};')

    for hijo in node.hijos:
        generar_dot(hijo, dot_lines, current_id, counter)

    if parent_id is None:
        dot_lines.append("}")
        return "\n".join(dot_lines)

if __name__ == "__main__":
    if tokens_list[-1]['type'] != '$':
        tokens_list.append({'type': '$', 'lexeme': '$', 'line': 0, 'column': 0})

    tabla = cargar_tabla_ll1('tabla.csv') 
    resultado, arbol = parse_ll1(tokens_list, tabla)
    print(resultado)

    if arbol:
        print("\nÁrbol sintáctico:")
        arbol.imprimir()
        dot_code = generar_dot(arbol)
        with open("arbol.dot", "w") as f:
            f.write(dot_code)
        print("Archivo 'arbol.dot' generado correctamente.")
    else:
        print("No se generó el árbol debido a errores en el análisis sintáctico.")
