

def string_matchin_fbruta(texto, patron):
    """
    Encuentra la primera ocurrencia de un patrón en un texto usando el algoritmo de fuerza bruta.

    Argumentos:
        texto: La cadena principal en la que se va a buscar.
        patron: La subcadena que se desea buscar.

    Retorna:
        El índice inicial de la primera coincidencia, o -1 si no se encuentra ninguna.
    """
    n = len(texto)
    m = len(patron)
    
    # Iterar por todas las posiciones posibles de inicio en el texto
    for i in range(n - m + 1):
        # Supone que hay coincidencia en la posición actual
        match = True
        # Comparar caracteres del patrón con caracteres en el texto
        for j in range(m):
            if texto[i + j] != patron[j]:
                match = False
                break  # Pasa a la siguiente posicion si no encuentra diferencia
        if match:
            return i  # Si todos los caracteres coinciden, devuelve indice inicial

    return -1  # No se encontró coincidencia después de revisar todas las posiciones

