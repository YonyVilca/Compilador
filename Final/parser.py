import csv

class Node:
    def __init__(self, nombre, token=None):
        self.nombre = nombre
        self.token = token  
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

    def imprimir(self, nivel=0):
        sangria = '  ' * nivel
        if self.token:
            print(f"{sangria}{self.nombre} → '{self.token['lexema']}'")
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
                    # Elimina "NO_TERMINAL ->" si lo contiene
                    if produccion.startswith(f"{no_terminal} ->"):
                        produccion = produccion.replace(f"{no_terminal} ->", "").strip()
                    simbolos = produccion.split()
                else:
                    simbolos = []
                tabla[no_terminal][terminal] = simbolos

        return tabla


def cargar_tokens_desde_csv(ruta_csv):
    tokens = []
    with open(ruta_csv, newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            tokens.append({
                'lexema': fila['lexema'].strip(),
                'linea': int(fila['linea']),
                'columna': int(fila['columna']),
            })
    tokens.append({'lexema': '$', 'linea': 0, 'columna': 0})
    return tokens

# LL(1)
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
        current_token = tokens[index]['lexema']
        linea = tokens[index]['linea']
        columna = tokens[index]['columna']

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

    if index >= len(tokens):
            return "✅ Cadena aceptada", nodo_raiz
    elif tokens[index]['lexema'] == '$':
        return "✅ Cadena aceptada", nodo_raiz
    else:
        return f" Error: tokens restantes sin analizar desde '{tokens[index]['lexema']}'", None


def generar_dot(node, dot_lines=None, parent_id=None, counter=[0]):
    if dot_lines is None:
        dot_lines = ["digraph G {", "  node [shape=box];"]

    current_id = f'node{counter[0]}'
    label = node.nombre
    if node.token:
        lexema = node.token['lexema']
        linea = node.token['linea']
        columna = node.token['columna']
        label += f"\\n'{lexema}'\\n[{linea},{columna}]"

    dot_lines.append(f'{current_id} [label="{label}"];')
    counter[0] += 1

    if parent_id:
        dot_lines.append(f'{parent_id} -> {current_id};')

    for hijo in node.hijos:
        generar_dot(hijo, dot_lines, current_id, counter)

    if parent_id is None:
        dot_lines.append("}")
        return "\n".join(dot_lines)

# Ejecutar y probar
if __name__ == "__main__":
    tabla = cargar_tabla_ll1('tabla.csv')
    tokens = cargar_tokens_desde_csv('token.csv')
    resultado, arbol = parse_ll1(tokens, tabla)
    print(resultado)

    if arbol:
        print("\n🌳 Árbol sintáctico:")
        arbol.imprimir()

        dot_code = generar_dot(arbol)
        with open("arbol.dot", "w") as f:
            f.write(dot_code)
        print("📄 Archivo 'arbol.dot' generado correctamente.")
    else:
        print("❌ No se generó el árbol debido a errores en el análisis sintáctico.")
