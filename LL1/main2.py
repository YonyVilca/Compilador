import csv

def cargar_tabla_ll1(ruta_csv):
    with open(ruta_csv, newline='') as archivo:
        lector = csv.reader(archivo)
        encabezados = next(lector)[1:]
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
    tokens.append({'lexema': '$', 'linea': 0, 'columna': 0}) 
    return tokens


def parse_ll1(tokens, tabla_ll1):
    stack = ['$', 'E']
    index = 0
#bucle principal
    while stack:
        if index >= len(tokens):
            return "Error: entrada terminada inesperadamente"
#Se extrae el símbolo superior de la pila y se asigna a top
        top = stack.pop()
        #Se obtiene el lexema del token actual utilizando index.
        current_token = tokens[index]['lexema']
        linea = tokens[index]['linea']
        columna = tokens[index]['columna']
        #Se obtiene el lexema del token actual utilizando index.
        if top in tabla_ll1:
            #Se comprueba si top es un no terminal que se encuentra en la tabla.
            
            produccion = tabla_ll1[top].get(current_token, [])
            #Se busca la producción correspondiente en la tabla utilizando el current_token. Si no hay producción
            if not produccion:
                return f" Error en token '{current_token}' (línea: {linea}, columna: {columna}): sin producción para [{top}, {current_token}]"
            elif produccion == ['e'] or produccion == ['ε']:
                continue
            else:
                for simbolo in reversed(produccion):
                    stack.append(simbolo)
#Si top coincide con current_token, se extrae de la pila, y se avanza al siguiente token incrementando index.
        elif top == current_token:
            index += 1
        else:
            return f"Error en token '{current_token}' (línea: {linea}, columna: {columna}): se esperaba '{top}'"

    if index >= len(tokens):
        return "Cadena aceptada"
    elif tokens[index]['lexema'] == '$':
        return "Cadena aceptada"
    else:
        return f"Error: tokens restantes sin analizar desde '{tokens[index]['lexema']}'"

if __name__ == "__main__":
    tabla = cargar_tabla_ll1('hoja1.csv')
    tokens = cargar_tokens_desde_csv('token.csv')
    resultado = parse_ll1(tokens, tabla)
    print(resultado)
