import sqlite3

def conexion_a_base_de_datos():
    ruta = 'C:\\Users\\angel\\Desktop\\portafolio\\base_de_datos.db'
    return ruta

def conectar_base_de_datos(ruta):
    try:
        conexion = sqlite3.connect(ruta)
        return conexion
    
    except sqlite3.Error:
        raise sqlite3.Error