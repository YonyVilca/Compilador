import csv

def cargar_tabla_ll1(ruta_csv):
    with open(ruta_csv, newline='') as archivo:
        lector = csv.reader(archivo)
        encabezados = next(lector)[1:]  # omitir columna vacía inicial
        tabla = {}
        for fila in lector:
            no_terminal = fila[0]
            producciones = [celda.strip() for celda in fila[1:]]
            tabla[no_terminal] = {
                terminal: produccion.split() if produccion else []
                for terminal, produccion in zip(encabezados, producciones)
            }
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
    tokens.append({'lexema': '$', 'linea': 0, 'columna': 0})  # Token de fin
    return tokens


def parse_ll1(tokens, tabla_ll1):
    stack = ['$', 'E']
    index = 0
    paso = 1

    print(f"{'Paso':<4} {'Pila':<30} {'Entrada':<30} {'Acción'}")

    while stack:
        if index >= len(tokens):
            print(f"{paso:<4} {'':<30} {'':<30} Error: entrada terminada inesperadamente")
            return

        top = stack.pop()
        current_token = tokens[index]['lexema']
        linea = tokens[index]['linea']
        columna = tokens[index]['columna']
        pila_str = ' '.join(stack[::-1])
        entrada_str = ' '.join([t['lexema'] for t in tokens[index:]])

        if top in tabla_ll1:
            produccion = tabla_ll1[top].get(current_token, [])
            if not produccion:
                print(f"{paso:<4} {pila_str:<30} {entrada_str:<30} Error en token '{current_token}' (línea: {linea}, columna: {columna}): sin producción para [{top}, {current_token}]")
                return
            elif produccion == ['e'] or produccion == ['ε']:
                print(f"{paso:<4} {pila_str:<30} {entrada_str:<30} {top} → ε")
                paso += 1
                continue
            else:
                print(f"{paso:<4} {pila_str:<30} {entrada_str:<30} {top} → {' '.join(produccion)}")
                for simbolo in reversed(produccion):
                    stack.append(simbolo)
                paso += 1

        elif top == current_token:
            print(f"{paso:<4} {pila_str:<30} {entrada_str:<30} match '{top}'")
            index += 1
            paso += 1

        else:
            print(f"{paso:<4} {pila_str:<30} {entrada_str:<30} Error en token '{current_token}' (línea: {linea}, columna: {columna}): se esperaba '{top}'")
            return
    
    
    if index >= len(tokens):
        print(f"{paso:<4} {'':<30} {'':<30} Cadena aceptada")
    elif tokens[index]['lexema'] == '$':
        print(f"{paso:<4} {'':<30} {'$':<30} Cadena aceptada")
    else:
        print(f"{paso:<4} {'':<30} {' '.join([t['lexema'] for t in tokens[index:]]):<30} Error: tokens restantes sin analizar")



if __name__ == "__main__":
    tabla = cargar_tabla_ll1('hoja1.csv')
    tokens = cargar_tokens_desde_csv('token.csv')

    print("\n🔍 Análisis desde token.csv\n")
    parse_ll1(tokens, tabla)
