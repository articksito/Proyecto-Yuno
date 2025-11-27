from db_connection import *
from terminal_receta import *
import sys
import os
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
carpeta_padre = os.path.dirname(carpeta_actual)
sys.path.append(carpeta_padre)


class consulta():
    def __init__(self):
        self.conexion=Conexion()
        self.receta=receta()
    
    def realizar_consulta(self):
        try:
            consultorio=input('Consultorio donde se realizara:')
            motivo=input('Motivo de la consulta:')
            metodo_pago=input('Metodo de pago:')
            id_veterinario=int(input('Id del veterinario asignado:'))
            id_mascota=int(input('Id de la mascota:'))
            receta=int(self.receta.insertar_receta())
            id_cita=int(input('Id de la cita:'))
            fecha=input('Fecha del dia:')
            hora=input('Hora del dia:')
            
            datos=(consultorio,motivo,metodo_pago,id_veterinario,id_mascota,receta,id_cita,fecha,hora)
            clumnas=('consultorio','motivo','metodo_pago','fk_veterinario','fk_mascota','fk_receta','fk_cita','fecha','hora')
            table='consulta'
                
            self.conexion.insertar_datos(table,datos,clumnas)
            input('Dale Enter')
                
        except Exception as Error:
            print(f"Error en cliente: {Error}")
            input('Dale Enter')
            
        finally:
            self.conexion.limpiar_terminal()