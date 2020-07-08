"""
Modulo principal del programa, en el que
quedan definidas la funcion principal y
donde se realiza el preprocesamiento de los
archivos recibidos en programas.txt y se
dispone la interfaz de usuario que permitira
acceder a cada una de las funcionalidades
"""

import manejo_imports
import lista_funciones
import generar_archivos_csv
import ordenar
import os
import arbol_invocacion

CARPETA_FUNCIONES_ORDENADAS = "funciones"
menu = ["1. Panel general de funciones",
        "2. Consulta de funciones",
        "3. Analizador de reutilizacion de codigo",
        "4. Arbol de invocacion",
        "5. Informacion por desarrollador"]

def preprocesamiento(programas):
  """[Autor: Elian Foppiano]"""
  ordenar.ordenar(programas)
  generar_archivos_csv.generar_csv()  
  manejo_imports.generar_lista_imports(programas)
  lista_funciones.generar_lista_funciones(programas)
  
def mostrar_menu():
  """[Autor: Elian Foppiano]"""
  print("Trabajo Practico".center(100, "_"))
  print("Algoritmos y Programacion I".center(100, "_"))
  print("Grupo Ballenato".rjust(100, " "))
  for linea in menu:
    print(linea)
  opcion = input("Opcion: ")

  return opcion

def funcion_principal():
  programas = open("programas.txt")
  preprocesamiento(programas)
  programas.close()
  opcion = mostrar_menu()
  if opcion == "4":
    arbol_invocacion.generar_arbol()

#-------Invocacion de la funcion principal-------#
funcion_principal()