from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from modelos.modelo_administrador import Admin
from http import HTTPStatus
from funciones.funciones_admin import *
from datetime import datetime, timedelta
import uuid
from jose import jwt
from secret.semilla import *
from base_de_datos.conexion import *
from errores.http_errores import *
import sqlite3
router = APIRouter()




@router.post('/crear/admin')
async def admin(admin_json:dict):
    admin = Admin(**admin_json)
    añadir_admin(admin)
    return 'creado'
    


oauth2_administrador = OAuth2PasswordBearer(tokenUrl='/login/administrador')

@router.post('/login/administrador')
async def administrador(form: OAuth2PasswordRequestForm = Depends(), conn: str = Depends(conexion_a_base_de_datos)):
    try:
        db = conectar_base_de_datos(conn)
        with db:
            chek_credenciales = chek_credenciales_admin(form.username, form.password, db)  # Verificamos las credenciales mediante la función.

            if chek_credenciales:
                
                expire = datetime.utcnow() + timedelta(minutes=160)  # Creamos el tiempo de expiración del token.
                tiempo_expiracion_str = expire.strftime('%Y-%m-%d %H:%M:%S')  # Lo convertimos en str.
                sesion_id = str(uuid.uuid4())  # Creamos un valor único para cada sesión.
                
                token = {    # Creamos el token.
                    'sub': form.username,
                    'expiracion': tiempo_expiracion_str,
                    'sesion_id': sesion_id,
                    'rol': 'administrador'
                }

                token_encriptado = jwt.encode(token, secret_key, algorithm=ALGORITHM)  # Codificamos el token.

                return {'token': token_encriptado}  # Retornamos el token como un json.
            
    except AuthenticationError:  # Capturamos esta excepción personalizada que se lanza en caso de que las credenciales sean incorrectas.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales incorrectas')  # Lanzamos la excepción.
    
    except sqlite3.Error:  # Capturamos cualquier error que provenga de la base de datos.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='500 internal server error')  # Lanzamos la excepción.
        
    except Exception:  # Capturamos algún error genérico.
        # Manejar otros errores genéricos.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error interno del servidor')  # Lanzamos la excepción.
        
            