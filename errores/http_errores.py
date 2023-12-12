from fastapi import HTTPException

# creamos la clase que lanza el error 401 que hereda de HTTPException
class AuthenticationError(HTTPException):
    def __init__(self,detail = 'credenciales invalidas',status_code = 401): # creamos el constructor ya que con los valores asignados 
        self.detail = detail
        self.status_code = status_code
        super().__init__(status_code=self.status_code,detail=self.detail) # llamamos el metodo super con el valor de esta clase 
        