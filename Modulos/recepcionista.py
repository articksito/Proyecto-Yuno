
from db_connection import *

class Recepcionista:
    def __init__(self):
        self.nosense=''

    def insertar_datos_cliente(self):
        
        try:
            nombre=input('Nombre:')
            apellido=input('Apellido:')
            direccion=input('Direccion:')
            correo=input('Correo electronico:')
            telefono=int(input('Numero de telefono:'))
            datos=(nombre,apellido,direccion,correo,telefono)

            sql=f'INSERT INTO cliente(nombre,apellido,direccion,correo,telefono) VALUES (%s,%s,%s,%s,%s);'
            conexion=Conexion()
            conexion.insertar_datos(sql,datos)

            
        except:
            print("Error")


    def agendar_citas(self):
        pass
    def ver_registros(self):
        pass

def main():
    r=Recepcionista()
    r.insertar_datos_cliente()

main()