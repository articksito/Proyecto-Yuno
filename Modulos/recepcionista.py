
from db_connection import *

class Recepcionista:
    def __init__(self,clave,nombre):
        pass
    def insertar_datos_cliente(self):
        nombre=input('Nombre:')
        apellido=input('Apellido:')
        direccion=input('Direccion:')
        correo=input('Correo electronico:')
        telefono=int(input('Numero de telefono:'))

        sql=f'INSERT INTO (nombre,apellido,direccion,correo,telefono) VALUES ({nombre},{apellido},{direccion},{correo},{telefono})'
        conexion=Conexion()
        conexion.insertar_datos(sql)


    def agendar_citas(self):
        pass
    def ver_registros(self):
        pass

a=Recepcionista
a.insertar_datos_cliente()