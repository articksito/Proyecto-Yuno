from db_connection import *

class Veterinario:
    def __init__(self):
        self.conexion1=Conexion()
        
    def menu_veterinario(self):
        while True:
            try:
                print("Menu mascotas")
                print("1.Consultar veterinarios\n2.Salir")
                    
                opcionC = int(input("Elije la opcion que desees elegir: ")) 
                match opcionC:
                    case 1:
                        self.consultar_veterinarios()
                    case 2:
                        break
            except ValueError:
                    print("Error: Debe ingresar un número válido")
                
    def consultar_veterinarios(self):
        try:
            columnas=self.conexion1.Select_users(table='veterinario')
            for colum in columnas:
                print('\t'.join(map(str,colum)))

        except Exception as a:
            print (f'Error al consultar veterinarios: {a}')