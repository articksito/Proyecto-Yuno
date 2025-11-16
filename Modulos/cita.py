from db_connection import *

class citas:
    def __init__(self):
        self.conexion1=Conexion()
        
    def menu_citas(self):
        print("Bienvenido al menu de citas")
        while True:
            try:    
                    print("1. Crear cita")
                    print("2. Editar las citas\n3.Eliminar cita\n4.Consultar citas")
                    opcionC = int(input("Elije la opcion que desees elegir: "))
                    match opcionC:
                        case 1:
                            self.crear_cita()
                        case 2:
                            self.modificar_cita()
                        case 3:
                            self.eliminar_cita()
                        case 4:
                            self.consultar_citas()
                        case 5:
                            break
            except ValueError:
                    print("Error: Debe ingresar un número válido")
                     
                
    def crear_cita(self):
        try:
            fecha=input('Pon la fecha:')
            hora=input('Pon hora:')
            estado=input('El estado del animal:')
            motivo=input('Motivo:')
            mascota=int(input('Id de mascota:'))
            veterinario=int(input('Id de veterinario:'))
            
            datos=(fecha,hora,estado,motivo,mascota,veterinario)
            columnas=('fecha','hora','estado','motivo','fk_mascota','fk_veterinario')
            table='cita'

            self.conexion1.insertar_datos(table,datos,columnas)

        except Exception as a:
            print(f'Error al crear cita: {a}')

    def modificar_cita(self):
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

            self.conexion1.editar_registro(id,datos,tabla='cita',id_columna='id_cita')
        except Exception as a:
            print(f'Error al modificar cita: {a}')
    
    def eliminar_cita(self):
        try:
            id=int(input('Id de la cita a eliminar:'))
            self.conexion1.eliminar_registro(id,tabla='cita',id_columna='id_cita')

        except Exception as a:
            print(f'Error al eliminar cita: {a}')
                
    def consultar_citas(self):
        try:
            columnas=self.conexion1.Select_users(table='cita')
            for colum in columnas:
                print('\t'.join(map(str,colum)))

        except Exception as a:
            print (f'Error al consultar citas: {a}')
