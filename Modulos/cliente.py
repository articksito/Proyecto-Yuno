from db_connection import *

class cliente():

    def __init__(self):
        self.conexion=Conexion()

    def insertar_datos_cliente(self):
        try:
            nombre=input('Nombre:')
            apellido=input('Apellido:')
            direccion=input('Direccion:')
            correo=input('Correo electronico:')
            telefono=int(input('Numero de telefono:'))
            datos=(nombre,apellido,direccion,correo,telefono)

            sql=f'INSERT INTO cliente(nombre,apellido,direccion,correo,telefono) VALUES (%s,%s,%s,%s,%s);'
            
            self.conexion.insertar_datos(sql,datos)
            
        except:
            print("Error")

    def ver_registro_cliente(self):
        tabla=input("Tabla:")
        datos=(tabla)
        
        registro=self.conexion.Select_users()
        
        for row in registro:
                    print('\t'.join(map(str, row)))

def main():
    r=cliente()
    r.ver_registro_cliente()

main()

