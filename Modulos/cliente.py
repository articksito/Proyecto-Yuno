from db_connection import *

class cliente():

    def __init__(self):
        self.conexion=Conexion()
    
    def mini_main(self):
         #Creen interfaz.
         self.ver_registro_cliente()

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
        try:
            tabla='cliente'
            registro=self.conexion.Select_users(tabla)
            
            for row in registro:
                        print('\t'.join(map(str, row)))
        except:
             print("Error")
            
    def editar(self):
        
        try:
            datos=[]
            id=int(input('ID:'))  

            while True:
                columna=input('Nombre de la columuna:')
                datos.append(columna)
                cerrar=int(input('Son todos? (1 para si)'))
                
                if cerrar==1:
                    break 

            self.conexion.editar_registro(id,datos,tabla='cliente')
        except:
             print("Error")
 
def main():
    r=cliente()
    r.mini_main()

main()

