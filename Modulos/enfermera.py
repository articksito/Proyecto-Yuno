from cita import *
from db_connection import *
from mascota import *


class Enfermera:
    def __init__(self):
        self.conexion=Conexion()
            

    def menu_enfermera(self):
            while True:
                try:
                    opcionE = int(input("""1.Consultar informacion de citas\n2.Consultar imformancion de pacientes
3.Actualizar diagnostico\n4.Cambiar contraseña\n5.Agregar medicina a farmacia\n6.Salir\nIngrese una opción: """))

                    match opcionE:
                        case 1:
                            self.consulat_citas()
                        case 2:
                            self.consultar_paciente()
                        case 3:
                            self.actualizar_diagnostico() 
                        case 4:
                            self.conexion.cambiar_contraseña()
                        case 5:
                              self.agregar_medicina()
                        case 5:
                              break
                        case __:
                              print('Pon el numero correcto.')
                      
                      
                except Exception as a:
                    print(f'Error en el menu de enfermera/o')
    
    def consulat_citas(self):
         citas1=citas()
         citas1.consultar_citas()
    def consultar_paciente():
        mascota1=Mascota()
        mascota1.consultar_mascota()

    def actualizar_diagnostico():
        ruta_expediente='/home/owner_jose/Proyecto-Yuno/diagnostico.txt'
        comando_expediente=input('Agrega algo:')
        with open(ruta_expediente, 'a') as f:
            f.write(comando_expediente)

    def agregar_medicina(self):
        try:
            nombre=input('Nombre de la medicina:')
            tipo=input('Tipo de medicina:')
            composicion=input('Composicion del medicamento:')
            dosis_recomendada=input('Dosis recoemndada del medicamento:')
            via_administracion=input('Se administra por:')
            
            datos=(nombre,tipo,composicion,dosis_recomendada,via_administracion)
            columnas=('nombre','tipo','composicion(mg)','dosis_recomendada','via_administracion')
            table='medicamento'

            self.conexion.insertar_datos(table,datos,columnas)

        except Exception as a:
             print(f'Error al agregar medicina: {a}')
    
    def consultar_medicamento(self):
        try:
            columnas=self.conexion.Select_users(table='medicamento')
            for colum in columnas:
                print('\t'.join(map(str,colum)))

        except Exception as a:
            print (f'Error al consultar medicamentos en repertorio: {a}')
