from db_connection import *
from consulta import *

class Veterinario:
    def __init__(self):
        self.conexion1=Conexion()
        self.consulta=consulta()
        
    def menu_veterinario(self):
        while True:
            try:
                print("Menu mascotas")
                print("""1.Consultar veterinarios\n2.Realizar consulta\n3.Salir""")
                    
                opcionC = int(input("Elije la opcion que desees elegir: ")) 
                match opcionC:
                    case 1:
                        self.consultar_veterinarios()
                    case 2:
                        self.realizar_consulta()
                    case 3:
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
        
    def realizar_consulta(self):
        self.consulta.realizar_consulta()
        
        