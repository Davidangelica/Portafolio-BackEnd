from modelos.modelo_administrador import Admin, AdminDB,sesion_admin
import bcrypt
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlite3 import Connection
from errores.http_errores import *
import sqlite3


def añadir_admin(admin: Admin):
    salt = bcrypt.gensalt()
    contraseña_cifrada = bcrypt.hashpw(admin.contraseña.encode('utf8'), salt=salt)
    admin_dict = dict(admin)
    admin_dict['contraseña'] = contraseña_cifrada
    admin_db = AdminDB(**admin_dict)
    admin_db.fecha_de_creacion = datetime.now()
    
    try:
        sesion_admin.add(admin_db)
        sesion_admin.commit()
        sesion_admin.close()
        
    except SQLAlchemyError as e:
        sesion_admin.rollback()
        raise RuntimeError(f"No se pudo añadir el admin: {str(e)}")
    



def chek_credenciales_admin(nombre, contrasena_plana: str, conn: Connection) -> bool:
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT contraseña FROM admins WHERE nombre = ?', (nombre,))
        resultado = cursor.fetchone()

        if resultado:
            hash_contrasena = resultado[0]
            if bcrypt.checkpw(contrasena_plana.encode('utf-8'), hash_contrasena):
                return True
            else:
                raise AuthenticationError('Credenciales inválidas')
        
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail='Error en la base de datos')
