from cita import *
from mascota import *
from Sesion import *

class Enfermera:
    def __init__(self):
        self.sesion_opciones=sesion()
            

    def menu_enfermera(self):
            while True:
                try:
                    opcionE = int(input("""1.Consultar informacion de citas\n2.Consultar imformancion de pacientes
3.Actualizar diagnostico\n4.Opciones de sesion\n5.Salir\nIngrese una opción: """))

                    match opcionE:
                        case 1:
                            self.consulat_citas()
                        case 2:
                            self.consultar_paciente()
                        case 3:
                            self.actualizar_diagnostico() 
                        case 4:
                            self.sesion() 
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

    def sesion(self):
         self.sesion_opciones()
        