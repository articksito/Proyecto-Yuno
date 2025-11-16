from db_connection import *

class Mascota:
    def __init__(self):
        self.conexion1=Conexion()
        
    def menu_mascotas(self):
        while True:

            try:
                print("Menu mascotas")
                print("1.Añadir mascota\n2.Consultar mascotasa\n3.Editar registro de mascota\n4.Salir")
                    
                opcionC = int(input("Elije la opcion que desees elegir: ")) 
                match opcionC:
                    case 1:
                        self.añadir_mascota()
                    case 2:
                        self.consultar_mascota()
                    case 3:
                        self.modificar_mascota()
                    case 4:
                        break
            except ValueError:
                    print("Error: Debe ingresar un número válido")
                
    def añadir_mascota(self):
        try:
            nombre=input("Nombre de la mascota:")
            edad=int(input("Edad del animal:"))
            peso=input("Peso de la mascota:")
            id_cliente=int(input('Id del cliente:'))
            id_tipo_animal=int(input('Id del tipo de mascota:'))
            
            datos=(nombre,edad,peso,id_cliente,id_tipo_animal)
            columnas=('nombre','edad','peso','fk_cliente','fk_tipo_animal')
            table='mascota'

            self.conexion1.insertar_datos(table,datos,columnas)

            ruta_expediente='/home/owner_jose/Proyecto-Yuno/expediente.txt'
            comando_expediente=f'{datos}'
            with open(ruta_expediente, 'a') as f:
                f.write(comando_expediente)

        except Exception as a:
            print(f'Error al añadir mascota: {a}')

    def consultar_mascota(self):
        try:
            columnas=self.conexion1.Select_users(table='mascota')
            for colum in columnas:
                print('\t'.join(map(str,colum)))

        except Exception as a:
            print (f'Error al consultar mascotas: {a}')

    def modificar_mascota(self):
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

            self.conexion1.editar_registro(id,datos,tabla='mascota',id_columna='id_mascota')

        except Exception as a:
            print(f'Error al modificar mascota: {a}')
