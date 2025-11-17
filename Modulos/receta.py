from db_connection import *

class receta:
    def __init__(self):
        self.conexion=Conexion()
    
    def insertar_receta(self):
        try:
            print('\nLa receta\n')
            indicaciones=input('Indicaciones de uso:')

            datos=(indicaciones,)
            clumnas=('indicaciones',)
            table='receta'
                
            devolver=self.conexion.insertar_datos(table,datos,clumnas)

            if devolver:
                self.agregar_medicamentos(devolver)
            
            ruta_expediente='/home/owner_jose/Proyecto-Yuno/diagnostico.txt'
            comando_expediente=f'{datos}'
            with open(ruta_expediente, 'a') as f:
                f.write(comando_expediente)

            return devolver

        except Exception as a:
            print(f'Error en receta:{a}')
        
    def agregar_medicamentos(self, id_receta):
        while True:
            try:
                id_medicamento=int(input('Id del medicamento: (0 para cerrar)'))

                if id_medicamento==0:
                    break

                cantidad=int(input('Cantidas de la dosis'))
                datos_intermedios = (id_receta, id_medicamento, cantidad)
                columnas_intermedias = ('fk_receta', 'fk_medicamento', 'cantidad')
                self.conexion.insertar_datos('receta_medicamento',datos_intermedios,columnas_intermedias)

            except Exception as a:
                print(f'Error al agregar medicamentos {a}')
        