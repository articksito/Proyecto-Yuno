from db_connection import *

class cliente():

    def __init__(self):
        self.conexion=Conexion()
    
    def manu_cliente(self):
         try:            
            while True:
                self.conexion.limpiar_terminal()

                opcion=int(input("Elige\n1.Registrar cliente\n2.Clientes registrados\n3.editar registro de cliente\n4.Para eliminar a un cliente\n5.Salir\n:"))
                
                match opcion:
                    case 1:
                        self.insertar_datos_cliente()
                    case 2:
                        self.ver_registro_cliente()
                    case 3:             
                        self.editar_cliente()
                    case 4:
                        self.eliminar_cliente()
                    case 5:
                        break
                    case __:
                        print("Equivocado")
         except Exception as a:
             print(f'Error en la seleccion: {a}')


    def insertar_datos_cliente(self):
        self.conexion.limpiar_terminal()

        try:
            nombre=input('Nombre:')
            apellido=input('Apellido:')
            direccion=input('Direccion:')
            correo=input('Correo electronico:')
            telefono=int(input('Numero de telefono:'))

            datos=(nombre,apellido,direccion,correo,telefono)
            clumnas=('nombre','apellido','direccion','correo','telefono')
            table='cliente'
            
            self.conexion.insertar_datos(table,datos,clumnas)
            
        except Exception as Error:
            print(f"Error en cliente: {Error}")

    def ver_registro_cliente(self):
        self.conexion.limpiar_terminal()

        try:
            tabla='cliente'
            registro=self.conexion.Select_users(tabla)
            
            for row in registro:
                        print('\t'.join(map(str, row)))
        except:
             print("Error")
            
    def editar_cliente(self):
        self.conexion.limpiar_terminal()
        
        try:
            datos={}
            id=int(input('ID:'))  

            while True:
                columna=input('Nombre de la columuna:').strip()
                valor=input(f'nuevo valor({columna}):')

                datos[columna]=valor

                cerrar=int(input('Son todos? (1 para si)'))
                if cerrar==1:
                    break 

            self.conexion.editar_registro(id,datos,tabla='cliente',id_columna='id_cliente')
        except Exception as a:
             print(f"Error en editar: {a}")
        
    def eliminar_cliente(self):
        self.conexion.limpiar_terminal()
        
        try:
            id=int(input('Id de la cliente a eliminar:'))
            self.conexion.eliminar_registro(id,tabla='cliente',id_columna='id_cliente')

        except Exception as a:
            print(f'Error al eliminar cliente: {a}')
 
