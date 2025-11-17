from db_connection import *

class receta:
    def __init__(self):
        self.conexion=Conexion()
    
    def insertar_receta(self):
        try:
            print('\nLa receta\n')
            indicaciones=input('Indicaciones de uso:')
            medicamento=int(input('Pon la id del medicamento:'))

            datos=(indicaciones,medicamento)
            clumnas=('indicaciones','fk_medicamento')
            table='receta'
                
            devolver=self.conexion.insertar_datos(table,datos,clumnas)
            return devolver

        except Exception as a:
            print(f'Error en receta:{a}')
        