"""

    Asignatura: Geometría computacional 
    Subgrupo: 1
    Curso: 2023-2024
    Alumno: Jiménez Poyatos, Pablo
    Curso: 4 CC
    Carrera: Grado en matemáicas.
    Práctica 1. Código de Huffman y Teorema de Shannon

"""

# Importamos el módulo os y la funcion log_2

from os import path
from math import log2,e,sqrt
import cv2


# Creamos la clase Nodo y árbol de pares.

class Nodo:
    
    """
    Clase que representa un nodo en un árbol binario de pares.

    Atributos:
    - clave: Identificador único del nodo.
    - valor: Valor asociado al nodo.
    - iz: Referencia al hijo izquierdo del nodo.
    - dr: Referencia al hijo derecho del nodo.
    """
    
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.iz = None
        self.dr = None


class ArbolDePares:
    
    """
    Clase que implementa un árbol binario de búsqueda para pares clave-valor.

    Atributos:
    - raiz: Nodo raíz del árbol.

    Métodos:
    - insertar(clave, valor): Inserta un nodo con clave y valor en el árbol.
    - eliminar(clave, valor): Elimina el nodo con clave y valor del árbol.
    - encontrar_minimo(): Encuentra el nodo con el valor mínimo en el árbol.
    - nodos(): Devuelve la cantidad total de nodos en el árbol.
    - gen_dic_cod(): Genera un diccionario con el código binario de cada hoja.
    - inorden(): Imprime los nodos del árbol en orden inorden.
    """
    
    def __init__(self):
        self.raiz = None
        


    def insertar(self, clave, valor):
        """
       Inserta un nuevo nodo en el árbol.

       Parámetros:
       - clave (cualquier tipo comparable): La clave del nuevo nodo.
       - valor (cualquier tipo): El valor asociado al nuevo nodo.

       Descripción:
       Esta función inserta un nuevo nodo en el árbol binario de búsqueda. 
       Si el árbol está vacío, el nuevo nodo se convierte en la raíz. 
       Si el árbol no está vacío, la función busca la ubicación correcta para 
       el nuevo nodo basándose en la comparación de claves y valores.
       """
       
        self.raiz = self._insertar(self.raiz, clave, valor)


    def _insertar(self, nodo, clave, valor):
        """ Funcion auxiliar de insertar"""
        
        if nodo is None:
            return Nodo(clave, valor)
        
        if valor[0] < nodo.valor[0]:
            nodo.iz = self._insertar(nodo.iz, clave, valor)
        elif valor[0] > nodo.valor[0]:
            nodo.dr = self._insertar(nodo.dr, clave, valor)
        else:
            # En caso de igualdad, compara el segundo elemento de la tupla
            if valor[1] < nodo.valor[1]:
                nodo.iz = self._insertar(nodo.iz, clave, valor)
            elif valor[1] > nodo.valor[1]:
                nodo.dr = self._insertar(nodo.dr, clave, valor)
            else:
                pass

        return nodo

    

    def eliminar(self, clave, valor):
        """
        Elimina un nodo con la clave y valor dados del árbol.

        Parámetros:
        - clave (cualquier tipo comparable): La clave del nodo a eliminar.
        - valor (cualquier tipo): El valor asociado al nodo a eliminar.

        Descripción:
        Esta función busca y elimina un nodo con la clave y valor dados del 
        árbol binario de búsqueda. Si el nodo tiene dos hijos, se reemplaza 
        por el nodo mínimo del subárbol derecho.
        """
        
        self.raiz = self._eliminar(self.raiz, clave, valor)


    def _eliminar(self, nodo, clave, valor):
        """ Funcion auxiliar de insertar"""        
        if nodo is None:
            return None
        
        if valor[0] < nodo.valor[0]:
            nodo.iz = self._eliminar(nodo.iz, clave, valor)
        elif valor[0] > nodo.valor[0]:
            nodo.dr = self._eliminar(nodo.dr, clave, valor)
        else:
            # En caso de igualdad, compara el segundo elemento de la tupla
            if valor[1] < nodo.valor[1]:
                nodo.iz = self._eliminar(nodo.iz, clave, valor)
            elif valor[1] > nodo.valor[1]:
                nodo.dr = self._eliminar(nodo.dr, clave, valor)
            else:
                # Caso 1: Nodo sin hijos o con un solo hijo
                if nodo.iz is None:
                    return nodo.dr
                elif nodo.dr is None:
                    return nodo.iz

                # Caso 2: Nodo con dos hijos
                # Encontrar el sucesor inorden (mínimo en el subárbol derecho)
                nodo_minimo = self._encontrar_minimo(nodo.dr)
                nodo.clave = nodo_minimo.clave
                nodo.valor = nodo_minimo.valor
                nodo.dr = self._eliminar(nodo.dr, nodo_minimo.clave)

        return nodo
                
    
    
    def encontrar_minimo(self):
        """ Encuentra el nodo con el valor mínimo en el árbol."""   
        return self._encontrar_minimo(self.raiz)


    def _encontrar_minimo(self, nodo):
        """ Función auxiliar para encontrar el nodo mínimo"""
    
        while nodo.iz is not None:
            nodo = nodo.iz
        return nodo



    def nodos(self):
        """ Devuelve la cantidad total de nodos en el árbol."""   
        
        return self._nodos(self.raiz)


    def _nodos(self, nodo):
        """Función auxiliar de la funcion nodos"""
        
        if nodo is None:
            return 0
        else:
            izq = self._nodos(nodo.iz)
            dcha = self._nodos(nodo.dr)
            nod = 1 + izq + dcha
            return nod 
    
    
    
    def gen_dic_cod(self):
        """
        Genera un diccionario con el código de cada hoja (caracter), 
        utilizando un recorrido inorden.
        """
        dic_cod = {}
        self._gen_dic_cod(self.raiz, "", dic_cod)
        return dic_cod


    def _gen_dic_cod(self, nodo, codigo_actual, dic_cod):
        """Función auxiliar de la funcion gen_dic_cod"""
        if nodo is not None:    
            # Si el nodo es una hoja, agregar el código al diccionario
            if nodo.iz is None and nodo.dr is None:   
                dic_cod[nodo.clave] = codigo_actual
            
            # Recursión a la izquierda (0)
            self._gen_dic_cod(nodo.iz, codigo_actual + "0", dic_cod)  
            # Recursión a la derecha (1)
            self._gen_dic_cod(nodo.dr, codigo_actual + "1", dic_cod)   
            
            
                
    def inorden(self):
        """ Imprime los nodos del árbol en orden inorden."""
        self._inorden(self.raiz)


    def _inorden(self, nodo):
        """Función auxiliar para el recorrido inorden."""
        if nodo:
            self._inorden(nodo.iz)
            print(f"Clave: {nodo.clave}, Valor: {nodo.valor}")
            self._inorden(nodo.dr)



# Funciones para resolver la práctica 1.

def es_ruta_de_archivo(s):
    """
    Verifica si la cadena s corresponde a una ruta de archivo válida.

    Parámetros:
    - s (str): La cadena a verificar.

    Return:
    - bool: Si s es una ruta válida o no.
    """
    
    return path.isfile(s)


def leerFichero(nombre):
    """
    Lee el contenido de un archivo y lo devuelve como un string.

    Parámetros:
    - nombre (str): El nombre del archivo a leer.

    Return:
    str: El contenido del archivo.
    """
      
    with open(nombre, 'r',encoding="utf8") as file:
          contenido = file.read()           
    return contenido


def contenido(palabra): 
    """
    Si la entrada es una ruta de archivo, devuelve el contenido de un archivo.
    De lo contrario, devuelve la misma cadena.

    Parámetros:
    - palabra (str): La ruta de archivo o cadena.

    Return:
    str: El contenido del archivo o la cadena original.
    """
    
    if es_ruta_de_archivo(palabra):
        contenido = leerFichero(palabra)
    else:
        contenido = palabra        
    return contenido


def contar_frecuencias(cadena):
    """
    Cuenta las frecuencias y las primeras apariciones de los caracteres en una
    cadena.

    Parámetros:
    - cadena (str): La cadena de entrada.

    Return:
    tuple: Dos diccionarios, uno con las frecuencias y otro con las frecuencias
    y las primeras apariciones de cada caracter.
    """
    frec = {}
    primera_ap = {}
    contador = 0

    for carac in cadena:
        if carac in frec:
            frec[carac] += 1
        else:
            frec[carac] = 1
            primera_ap[carac] = contador
            
        contador += 1
    resultado = {carac: (frec[carac], primera_ap[carac]) for carac in frec}
    return resultado, frec


def arbol_frecuencias(dic):
    """
    Crea un árbol binario de busqueda de pares a partir de un diccionario.

    Parámetros:
    - dic (dict): El diccionario de frecuencias.

    Return:
    ArbolDePares: Un árbol binario de búsqueda de frecuencias.
    """
    
    arbol = ArbolDePares()
    for clave in dic:
        arbol.insertar(clave, dic[clave])
    return arbol
        
  
def plantar(nodo, ab_izq, ab_dch):
    """
    Crea un nuevo árbol uniendo un nodo con dos subárboles.

    Parámetros:
    - nodo (Nodo): El nodo raíz del nuevo árbol.
    - ab_izq (ArbolDePares o None): Subárbol izquierdo.
    - ab_dch (ArbolDePares o None): Subárbol derecho.

    Return:
    ArbolDePares: El nuevo árbol.
    """
    
    nuevo_arbol = ArbolDePares()
    nuevo_arbol.raiz = nodo
    if ab_izq is None:
        nuevo_arbol.raiz.iz = None
    else:
        nuevo_arbol.raiz.iz = ab_izq.raiz
        
    if ab_dch is None:
        nuevo_arbol.raiz.dr = None
    else:
        nuevo_arbol.raiz.dr = ab_dch.raiz
    return nuevo_arbol        


def add_dic_ab(min1,dic, iz, dr):
    """
    Agrega un nuevo árbol al diccionario.

    Parámetros:
    - min1 (Nodo): Nodo del árbol a agregar.
    - dic (dict): Diccionario de árboles.
    - iz (ArbolDePares o None): Subárbol izquierdo.
    - dr (ArbolDePares o None): Subárbol derecho.

    Return:
    dict: Diccionario actualizado.
    """
    
    if min1.clave not in dic:
        newNodo = Nodo(min1.clave, min1.valor)
        newArbol = plantar(newNodo, iz, dr)
        raizD = newArbol.raiz.clave
        dic[raizD] = newArbol
    return dic

        
def dic_arboles(arbol):
    """
    Construye un diccionario de árboles a partir de un árbol original. Esta 
    funcion escoge los dos valores con frecuencias mas pequeñas, crea un 
    arbol con esos nodos y lo añade al diccionario. 'Idea detras del algoritmo
    de Huffman'    

    Parámetros:
    - arbol (ArbolDePares): El árbol original.

    Return:
    dict: Diccionario de árboles.
    """
    
    dic = {}
    
    if arbol.nodos() == 1:
        min1 = arbol.encontrar_minimo()
        dic = add_dic_ab(min1, dic, None, None)
        
    else:
        while arbol.nodos() != 1:
            
            min1 = arbol.encontrar_minimo()
            arbol.eliminar(min1.clave, min1.valor)
            
            min2 = arbol.encontrar_minimo()
            arbol.eliminar(min2.clave, min2.valor)
            
            newchar = min1.clave + min2.clave
            newfrec = min1.valor[0] + min2.valor[0]
            newprior = min(min1.valor[1], min2.valor[1])
            newNodo = Nodo(newchar, (newfrec,newprior))
            arbol.insertar(newNodo.clave, newNodo.valor)
            
            
            dic = add_dic_ab(min1, dic, None, None)        
            dic = add_dic_ab(min2, dic, None, None)
            dic = add_dic_ab(newNodo, dic, dic[min1.clave], dic[min2.clave])
    
    return dic

    
def crear_palabra(dic_cambio, codif_Hauf):
    """
    Crea una palabra a partir de una codificación Huffman.

    Parámetros:
    - dic_cambio (dict): Diccionario de cambio.
    - codif_Hauf (str): La codificación Huffman.

    Return:
    str: La palabra decodificada.
    """
    
    palabra = ""
    codif = ""
    for i in range(len(codif_Hauf)):
        car = codif_Hauf[i]
        codif += car
        if codif in dic_cambio:
            palabra += dic_cambio[codif]
            codif = ""
    return palabra 

def codigo_Huffman(string):
    """
    Genera el diccionario de códigos Huffman y las frecuencias de caracteres.

    Parámetros:
    - string (str): Muestra con la que se crea el codigo de Huffman.

    Return:
    tuple: Un diccionario de códigos Huffman, otro con las frecuencias y otro 
    con las frecuencias y la primera vez que aparece cada caracter.
    """
    
    texto = contenido(string)
    frec, frec_SR = contar_frecuencias(texto)
    arbol_frec = arbol_frecuencias(frec)
    diccionario = dic_arboles(arbol_frec)
    
    ultimo = list(diccionario.keys())[-1]
    arbol = diccionario[ultimo]
    dic_traduccion = arbol.gen_dic_cod()
        
    return dic_traduccion, frec, frec_SR
    
    
def codificar_palabra(texto, dic_traduccion):
    """
    Codifica una palabra utilizando un diccionario de traducción.

    Parámetros:
    - texto (str): La palabra a codificar.
    - dic_traduccion (dict): Diccionario de traducción de caracteres a códigos.

    Return:
    str: La palabra codificada.
    """
    
    codificacion = ""
    for i in texto:
        codificacion += dic_traduccion[i]
        
    return codificacion
   

def decodificacion(codif_Hauf,dic_trad):
    """
    Decodifica una cadena Huffman utilizando un diccionario de traducción.

    Parámetros:
    - codif_Hauf (str): La cadena codificada con Huffman.
    - dic_trad (dict): Diccionario de traducción caracteres a códigos.

    Return:
    str: La cadena decodificada.
    """
    
    # Cambio las claves y los valores del diccionario.
    dic_cambio = dict(zip(dic_trad.values(), dic_trad.keys()))
    palabra = crear_palabra(dic_cambio, codif_Hauf)
    
    return palabra


def longitudMedia_entropia(palabra, codigo):
    """
    Calcula la longitud media, la entropía y la longitud total y el error de 
    un string utilizando un código dado.

    Parámetros:
    - palabra (str o dict): La palabra o diccionario de frecuencias.
    - codigo (dict): El código de cada caracter.

    Return:
    tuple: Una tupla con la longitud total, entropía, longitud media y error.
    """
    
    if isinstance(palabra, dict):
        frec = palabra
        num_caract = sum(list(frec.values()))
    else:
        frec_CR, frec = contar_frecuencias(palabra)
        num_caract = len(palabra)
        
    lista_claves = list(frec.keys())
    longitud = 0
    entropia = 0
    error = 0
    
    for i in lista_claves:
        frecI = frec[i]
        long = len(codigo[i])
        longitud += frecI*long
        prob = frecI/num_caract
        error += (log2(e*prob))**2
        entropia -= prob * log2(prob)
        
    error = 1/(len(lista_claves))**2 * sqrt(error)
    longitud_media = longitud / num_caract      
    return longitud, entropia, longitud_media, error
  

def comprobar_1TS(l,h):
    """
    Comprueba el Primer Teorema de Shanon.

    Parámetros:
    - l (float): Longitud media de un codigo binario usando Huffman.
    - h (float): Entropía del sistema.

    Return:
    bool: Si se cumple el Primer Teorema de Shanon con esos valores.
    """
    
    return h <= l and l < h + 1
    

def longitudCBU(string):
    """
    Calcula la longitud de un string despues de usar la codificacion binaria
    usual (ASCII).

    Parámetros:
    - string (str): La cadena de caracteres que pasamos a binario usual y 
                    medimos su longitud.

    Return:
    int: La longitud total en bits.
    """
    
    long = 0
    codif = ''
    for i in string:
        binario = bin(ord(i))
        long += len(binario) - 2
        codif += str(binario)[2:]
    return long, codif


def comprobarL(long,long_CBU):
    """
    Comprueba si la longitud total de la codificacion usando el codigo de 
    Huffman es menor que usando el codigo binario usual.

    Parámetros:
    - long (int): La longitud de la cadena usando Huffman.
    - long_CBU (int): La longitud de la cadena usando binario usual.

    Return:
    bool: Si la longitud usando Huffman es menor que usando binario usual.
    """
    
    return long <= long_CBU



# Soluciones
    
if __name__ == "__main__":
    
    # Apartado 1
    
    path1 = 'GCOM2024_pract1_auxiliar_esp.txt'
    path2 = 'GCOM2024_pract1_auxiliar_eng.txt'
    
    S_Es, frecEs, frecEs_SR = codigo_Huffman(path1)
    S_En, frecEn, frecEn_SR = codigo_Huffman(path2)
    
    long_Es, h_Es, l_Es, er_Es = longitudMedia_entropia(frecEs_SR, S_Es)
    
    long_En, h_En, l_En, er_En = longitudMedia_entropia(frecEn_SR, S_En)
    
    
    comprobacionEs = comprobar_1TS(l_Es,h_Es)
    comprobacionEn = comprobar_1TS(l_En,h_En)
    
    
    print(f'i) El codigo Huffman binario español: S_Es = {S_Es}')
    print('')
    print(f'El codigo Huffman binario inglés: S_En = {S_En}')
    print('')
    
    
    print(f'La longitud media en L(S_Esp) es {l_Es}')
    print(f'La longitud media en L(S_Eng) es {l_En}')
      
    
    print('')
    print("Por último, comprobamos si se satisface el Primer Teorema de " + 
          "Shannon. Para ello hay que comprobar que H(C) <= L(C) < H(C) + 1")
    print('')
    print(f"Para el sistema español: {comprobacionEs}. Tenemos que " +
          f"H(C) = {h_Es} <= L(C) = {l_Es} < H(C) + 1 = {h_Es + 1}.")
    print('')
    print(f"Para el sistema inglés: {comprobacionEn}. Tenemos que " + 
          f"H(C) = {h_En} <= L(C) = {l_En} < H(C) + 1 = {h_En + 1}.")
    print('')
    print(f'El error del calculo de la entropia para S_Es es {er_Es}.' +
          f'y para S_En, {er_En}.')
    
    
    # Apartado 2

    palabra = 'Lorentz'
    
    codif_Es = codificar_palabra(palabra, S_Es)
    long_Es, h_Es, l_Es, er_Es = longitudMedia_entropia(palabra, S_Es)
    long_CBU_Es, codif_BU = longitudCBU(palabra)
    comprobacion_Es = comprobarL(long_Es,long_CBU_Es) 
    
    codif_En = codificar_palabra(palabra, S_En)
    long_En, h_En, l_En, er_En = longitudMedia_entropia(palabra, S_En)
    long_CBU_En,codif_BU = longitudCBU(palabra)
    comprobacion_En = comprobarL(long_En,long_CBU_En) 
    
    
    print('')
    print('')    
    print(f"ii) La codificacion de la palabra {palabra} usando el código " +
          "español obtenido en el apartado anterior es:")
    print(f'S_Es : {codif_Es}')
    print('')
    print(f"La codificacion de la palabra {palabra} usando el código " + 
          "inglés obtenido en el apartado anterior es:")
    print(f'S_En : {codif_En}')
    print('')
    
    print("Por último vamos a comprobar que es más eficiente que el código " + 
          "binario usual. Para ello comprobamos que la codificacion de " + 
          f"Lorentz usando el codigo binario usual (ASCII) es: {codif_BU}")
    print('')
    print(f'Codificación de Huffman español : {long_Es} bits')
    print(f'Binario usual: {long_CBU_Es} bits')
    print(f"¿Es más eficiente?: {comprobacion_Es}. Hay una diferencia de " + 
          f"{long_CBU_Es - long_Es} bits.")
    print('')
    print(f'Codificación de Huffman ingles : {long_En} bits')
    print(f'Binario usual: {long_CBU_En} bits')
    print(f"¿Es más eficiente?: {comprobacion_En}. Hay una diferencia de " + 
          f"{long_CBU_En - long_En} bits")


    # Apartado 3
    
    palabra_Es = decodificacion(codif_Es, S_Es)
    palabra_En = decodificacion(codif_En, S_En)
    
    print('')
    print('')
    print("iii) La decodificación de los códigos obtenidos en el " +
          "apartado ii) son:")
    print('En español, decodificamos:')
    print(f'{codif_Es} y obtenemos {palabra_Es}')
    print('En inglés, decodificamos:') 
    print(f'{codif_En} y obtenemos {palabra_En}')
  



