COMILLAS_DOBLES = chr(34) * 3
COMILLAS_SIMPLES = chr(39) * 3
SALTO_LINEA = "/n/"


def leer_lineas_csv(archivo):
    """[Autor: Grupo Ballenato]
    [Ayuda: A partir de una linea de un .csv, devuelve una
    lista de todos los valores que esten separados por ",".]"""
    linea = archivo.readline().rstrip().split(",")
    return linea


def obtener_lista_funciones(marcador):
    """[Autor: Grupo Ballenato]
    [Ayuda: Genera una lista con las funciones
    definidas en el programa]"""
    """
    Parametros
    ----------
    marcador : bool
            Indica si el marcador principal "$" debe eliminarse del
            nombre de la funcion principal o no

    Returns
    -------
    lista de str
            Nombres de las funciones definidas en el programa
    """

    with open("fuente_unico.csv") as archivo:
        funciones = []
        linea = leer_lineas_csv(archivo)
        while linea[0]:
            if marcador == False:
                funciones.append(linea[0].replace("$",""))
            else:
                funciones.append(linea[0])
            linea = leer_lineas_csv(archivo)
    return funciones


def obtener_comentario_multilinea(linea, arch):
    """
    [Autor: Elian Daniel Foppiano]
    [Ayuda: Recorre el archivo recibido hasta que encuentra
    el final del comentario multilinea y lo devuelve formateado.]
    """
    """
    Parametros
    ----------
    linea : str
            Donde empieza el comentario multilinea
    arch : archivo, modo lectura
            Donde puede continuar el comentario multilinea

    Returns
    -------
    str
            Comentario multilinea con los saltos de linea reemplazados
            por el marcador "/n/"
    """

    # Si el comentario empieza y termina en la misma linea
    if linea.count(COMILLAS_DOBLES) == 2 or linea.count(COMILLAS_SIMPLES) == 2:
        comentario = linea.rstrip()
    else:  # El comentario tiene mas de una linea
        # Cambio el salto de linea por el marcador especial
        comentario = linea.rstrip() + SALTO_LINEA
        linea = arch.readline().rstrip()
        # Mientras no llegue al final del comentario
        while not linea.endswith((COMILLAS_DOBLES, COMILLAS_SIMPLES)):
            comentario += linea + SALTO_LINEA
            linea = arch.readline().rstrip()
        comentario += linea

    return comentario
