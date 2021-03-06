"""
Modulo que imprime una tabla de todas las funcionalidades de la aplicacion y le
pide al usuario el ingreso de un pedido que se ajuste al formato solicitado en
la consigna del pdf, esto le permite obtener la informacion que desee sobre una
funcion en especifico, sobre todas o solicitar la creacion de un archivo txt
con la informacion de ayuda asociada de todas las funciones limitada a 80
caracteres por linea
"""


import os
from universales import leer_lineas_csv
from universales import obtener_lista_funciones


def cortar_lista_funciones(funciones, largo):
    """[Autor: Santiago Marczewski]
    [Ayuda: Corta la lista de funciones en partes de cinco funciones de largo
    para facilitar el formateo de la tabla.]"""
    #Se corta la lista de funciones en partes de 5 funciones
    lista_cortada = [funciones[x:x+5] for x in range(0, len(funciones), 5)]
    #Si la ultima parte tiene menos de 5 funciones
    #Se agrega strings vacios hasta llegar a 5
    while len(lista_cortada[-1]) < 5: 
        lista_cortada[-1].append(" "*largo)
    return lista_cortada


def mostrar_tabla():
    """[Autor: Santiago Marczewski]
    [Ayuda: Imprime por pantalla una tabla de las funciones de la aplicacion
    formateado de manera similar a la tabla de built-in functions de la
    documentacion de Python.]"""
    funciones = obtener_lista_funciones(False)
    #Se calcula el largo que va a ocupar la funcion mas larga en la tabla
    largo = len(max(funciones, key=len)) + 1
    #Se corta la lista en partes de 5
    lista_cortada = cortar_lista_funciones(funciones, largo)
    #Se imprime la tabla y en el caso de funciones que sean mas cortas
    #Que la mas larga, se compensa con espacios en blanco
    for funcion in lista_cortada:
        print(("+" + "-"*largo)*5 + "+", sep="")
        print("|", funcion[0], " "*(largo-len(funcion[0])), "|",
              funcion[1], " "*(largo-len(funcion[1])), "|",
              funcion[2], " "*(largo-len(funcion[2])), "|",
              funcion[3], " "*(largo-len(funcion[3])), "|",
              funcion[4], " "*(largo-len(funcion[4])), "|", sep="")
    print(("+" + "-"*largo)*5 + "+", sep="")


def nro_linea(linea):
    """[Autor: Santiago Marczewski]
    [Ayuda: Recibe una linea, lee su marcador y devuelve en que linea debe ir]"""
    numero_linea = int(linea[1:linea.index("/", 1)])
    return numero_linea


def comparador_marcadores(instruccion, adicional):
    """[Autor: Santiago Marczewski]
    [Ayuda: Determina si una instruccion esta antes(1), despues(2)
    o en la misma linea(0) que un comentario adicional, comparando sus marcadores]"""
    nro_linea_instruccion = nro_linea(instruccion)
    nro_linea_adicional = nro_linea(adicional)

    if nro_linea_instruccion < nro_linea_adicional: #Si la instruccion va antes
        devolver = 1
    elif nro_linea_instruccion > nro_linea_adicional: #Si el comentario va antes
        devolver = 2
    else: #Si ambos van en la misma linea
        devolver = 0
    return devolver


def eliminar_marcador(linea):
    """[Autor: Santiago Marczewski]
    [Ayuda: Elimina el marcador de la linea pasada por parametro]"""
    #Buscamos la segunda barra
    segunda_barra = linea.index("/", 1)
    #Descartamos todo lo anterior a la segunda barra
    linea = linea[segunda_barra + 1:]
    return linea


def imprimir_formateado(linea):
    """[Autor: Santiago Marczewski]
    [Ayuda: Toma una linea y la imprime formateada correctamente,
    incluyendo sus comas y saltos de linea originales]"""
    #Eliminamos el marcador
    linea = eliminar_marcador(linea)
    #Reemplazamos marcadores de coma por comas reales
    #Y marcadores "/n/" por saltos de linea reales
    linea = linea.replace("/c/", ",").replace("/n/", "\n")
    print(linea)


def imprimir_codigo(instrucciones, adicionales):
    """[Autor: Santiago Marczewski]
    [Ayuda: Toma las instrucciones y los comentarios adicionales e imprime el bloque de codigo
    correspondiente tal como aparece en el codigo de la aplicacion]"""
    #Inicializamos los contadores de ambas listas
    i = j = 0
    #Mientras todavia queden lineas sin leer de ambas listas
    while i < len(instrucciones) and j < len(adicionales):
        #comparamos las lineas, imprimimos y aumentamos el contador segun corresponda
        control = comparador_marcadores(instrucciones[i], adicionales[j])
        if control == 1:
            imprimir_formateado(instrucciones[i])
            i += 1
        elif control == 2:
            imprimir_formateado(adicionales[j])
            j += 1
        else: #En caso de que vayan en la misma linea, le quitamos el marcador al comentario antes
            imprimir_formateado(instrucciones[i] + " " + eliminar_marcador(adicionales[j]))
            i += 1
            j += 1
    #Si quedan instrucciones sin leer
    while i < len(instrucciones):
        imprimir_formateado(instrucciones[i])
        i += 1
    #Si quedan comentarios sin leer
    while j < len(adicionales):
        imprimir_formateado(adicionales[j])
        j += 1


def sumar_largo_lista(lista):
    """[Autor: Santiago Marczewski]
    [Ayuda: Recibe una lista de palabras y devuelve una lista de cuantas se
    pueden poner por linea para no sobrepasar los 80 caracteres]"""
    largo_linea = []
    contador = 0 #Cuenta la cantidad de palabras
    contador_largo = 0 #Cuenta la cantidad de caracteres + espacios blancos
    for palabra in lista:
        #Si al sumar la siguiente palabra no sobrepasamos los 80 caracteres
        if contador_largo + (len(palabra) + 1) < 80:
            contador += 1
            contador_largo += (len(palabra) + 1)
        #Si al sumar la siguiente palabra sobrepasamos los 80 caracteres
        else:
            largo_linea.append(contador)
            contador = 0 #Reiniciamos el contador
            contador += 1
            contador_largo = 0 #Reiniciamos el contador
            contador_largo += (len(palabra) + 1)
    largo_linea.append(contador) #Agregamos el largo de la ultima linea
    return largo_linea
            
        
def limitar_largo_linea(texto_a_limitar, texto):
    """[Autor: Santiago Marczewski]
    [Ayuda: Recibe las lineas de la descripcion de ayuda y las devuelve
    formateadas y limitadas a 80 caracteres para la creacion del txt]"""
    #Transformamos nuestro string en un lista y borramos espacios de mas
    texto_a_limitar = texto_a_limitar.strip().split()
    #Obtenemos en cuantas palabras hay que separar nuestra lista
    largo_linea = sumar_largo_lista(texto_a_limitar)
    total = 0 #Cuenta hasta donde ya cortamos
    lineas_80 = [] #Lista cortada
    #El ciclo for se ejecuta segun cuantos cortes hay que hacer
    for i in range(len(largo_linea)):
        corte = texto_a_limitar[total : total + largo_linea[i]]
        lineas_80.append(corte)
        total += largo_linea[i]
    for linea in lineas_80: #Unimos e imprimimos las lineas
        print(" ".join(linea), file=texto)
        
        
def buscar_funcion(archivo, funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Busca una funcion por su nombre en el archivo pasado por parametro y
    devuelve toda la linea que le corresponde del csv.]"""
    archivo.seek(0)
    nombre_funcion = ""
    #Comparamos la funcion que buscamos con el primer campo de fuente_unico
    while nombre_funcion != funcion:
        linea = leer_lineas_csv(archivo)
        if linea[0].startswith("$"):
            nombre_funcion = linea[0][1:]
        else:
            nombre_funcion = linea[0]
    return linea


def mostrar_funcion(nombre, tipo, fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Toma una funcion y el tipo de pedido y muestra por pantalla la descripcion de ayuda, parametros,
    modulo y autor de la funcion, tomando los datos de los archivos csv pasados por parametro]"""
    """
    Parametros
    ----------
    nombre : str
            Nombre de la funcion que se quiere ver
    tipo : str
            Es uno de los caracteres que indica el tipo de pedido (? o #)
    fuente_unico : archivo csv
            Archivo con parte de la informacion de cada funcion
    comentarios : archivo csv
            Archivo con parte de la informacion de cada funcion
    """
    #Tomamos los datos necesarios
    info_fuente = buscar_funcion(fuente_unico, nombre)
    info_comentarios = buscar_funcion(comentarios, nombre)
    ayuda = info_comentarios[2]
    parametros = info_fuente[1]
    modulo = info_fuente[2]
    autor = info_comentarios[1]
    #Si se pide el bloque de codigo, tomamos los comentarios e instrucciones
    if tipo == "#":
        instrucciones = info_fuente[3:]
        adicionales = info_comentarios[3:]
    #Imprimimos todo
    print("="*80)
    print("--Funcion :", nombre)
    if ayuda:
        print("--", ayuda.replace("/n/", "\n").replace("/c/", ","), sep="")
    else:
        print("--Ayuda: No hay descripcion de ayuda disponible")
    if parametros != "()":
        print("--Parametros: ", parametros.replace("/c/", ","))
    else:
        print("--Parametros: No existen parametros")
    print("--Modulo: ", modulo)
    print("--Autor: ", autor)
    if tipo == "#":
        print("-"*80)
        print("--Codigo de la funcion:")
        imprimir_codigo(instrucciones, adicionales)


def mostrar_funcion_txt(nombre, texto, fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Toma una funcion y el tipo de pedido y envia al archivo ayuda_funciones.txt la descripcion de ayuda,
    parametros, modulo y autor de la funcion, tomando los datos de los archivos csv pasados por parametro]"""
    """
    Parametros
    ----------
    nombre : str
            Nombre de la funcion que se quiere ver
    texto : archivo txt
            Archivo de texto al que se quiere imprimir la informacion
    fuente_unico : archivo csv
            Archivo con parte de la informacion de cada funcion
    comentarios : archivo csv
            Archivo con parte de la informacion de cada funcion
    """
    #Tomamos los datos necesarios
    info_fuente = buscar_funcion(fuente_unico, nombre)
    info_comentarios = buscar_funcion(comentarios, nombre)
    ayuda = info_comentarios[2]
    parametros = info_fuente[1]
    modulo = info_fuente[2]
    autor = info_comentarios[1]
    #Imprimimos todo directamente al archivo ayuda_funciones.txt
    print("="*80, file=texto)
    print("--Funcion :", nombre, file=texto)
    if ayuda:
        ayuda = ("--" + ayuda.replace("/n/", " ").replace("/c/", ","))
        #Limitamos las lineas a 80
        limitar_largo_linea(ayuda, texto)
    else:
        print("--Ayuda: No hay descripcion de ayuda disponible", file=texto)
    if parametros != "()":
        parametros = ("--Parametros: " + parametros.replace("/c/", ","))
        #Limitamos las lineas a 80
        limitar_largo_linea(parametros, texto)
    else:
        print("--Parametros: No existen parametros", file=texto)
    print("--Modulo: ", modulo, file=texto)
    print("--Autor: ", autor, file=texto)


def mostrar_todo(tipo, imprimir, fuente_unico, comentarios):
    """[Autor: Santiago Marczewski]
    [Ayuda: Toma una funcion y el tipo de pedido y muestra por pantalla la informacion correspondiente (? o #)
    para todas las funciones de la aplicacion, tomando datos de los archivos csv pasados por parametro]"""
    """
    Parametros
    ----------
    tipo : str
            Es uno de los caracteres que indica el tipo de pedido (? o #)
    imprimir : bool
            Booleano que indica si hay que imprimir a txt o no
    fuente_unico : archivo csv
            Archivo con parte de la informacion de cada funcion
    comentarios : archivo csv
            Archivo con parte de la informacion de cada funcion
    """
    funciones = obtener_lista_funciones(False)
    #Si se pide imprimir al txt
    if imprimir:
        #Creamos el archivo ayuda_funciones.txt
        texto = open(os.path.join("funcionalidades",
                                  "ayuda_funciones.txt"), "w")
        print("Información asociada a las funciones de la aplicación: \n", file=texto)
        for funcion in funciones:
            mostrar_funcion_txt(funcion, texto, fuente_unico, comentarios)
        print("="*80, file=texto)
        texto.close()
        print("\n# El archivo ayuda_funciones.txt fue creado con exito.\n")
    #Sino imprimimos por pantalla
    else:
        for funcion in funciones:
            mostrar_funcion(funcion, tipo, fuente_unico, comentarios)
        print("="*80)


def procesar_pedido(funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Procesa el pedido del usuario y devuelve el nombre de la funcion
    solicitada, el tipo de pedido y si hay que imprimirlo a .txt o no]"""
    nombre = ""
    tipo = ""
    imprimir = ""
    if len(funcion.split()) == 1:  # Si el ingreso es de una palabra
        nombre = funcion[1:]
        tipo = funcion[0]
        imprimir = False
    elif len(funcion.split()) == 2:  # Si el ingreso tiene dos palabra
        pedido = funcion.split()
        nombre = pedido[1][1:]
        tipo = pedido[1][0]
        imprimir = pedido[0]
    return (nombre, tipo, imprimir)


def validar_funcion(funcion):
    """[Autor: Santiago Marczewski]
    [Ayuda: Verifica que la funcion pasada por parametro sea valida]"""
    valida = True
    funciones = obtener_lista_funciones(False)
    #Agregamos "todo" como otra opcion valida
    funciones.append("todo")
    nombre, tipo, imprimir = procesar_pedido(funcion)
    if nombre not in funciones:
        valida = False
    elif tipo not in ["?", "#"]:
        valida = False
    elif imprimir:
        #Si el pedido no es especificamente el mencionado
        #En la consigna, el ingreso es invalido
        if funcion != "imprimir ?todo":
            valida = False
    return valida


def funcionalidad_2():
    """[Autor: Santiago Marczewski]
    [Ayuda: Funcion principal de la funcionalidad, muestra la tabla, pide al usuario el ingreso de su pedido,
    lo valida y muestra la informacion correspondiente]"""
    #Abrimos los archivos
    fuente_unico = open("fuente_unico.csv")
    comentarios = open("comentarios.csv")
    #Mostramos la tabla por pantalla
    mostrar_tabla()
    #Pedimos un ingreso al usuario
    funcion = input("Ingrese una funcion: ")
    while funcion:
        #Si el pedido es valido
        if validar_funcion(funcion):
            nombre, tipo, imprimir = procesar_pedido(funcion)
            #Si se pidio todo
            if imprimir or nombre == "todo":
                mostrar_todo(tipo, imprimir, fuente_unico, comentarios)
            #Si se pidio una funcion especifica
            else:
                mostrar_funcion(nombre, tipo, fuente_unico, comentarios)
                print("=" * 80)
        #Si el pedido es invalido se pide de nuevo
        else:
            print("Ingreso invalido, intente nuevamente")
        #Si se termino un pedido con exito, se pide otro
        funcion = input("Ingrese una funcion: ")
    #Cerramos los archivos
    fuente_unico.close()
    comentarios.close()
