from cita import *
from mascota import *

class Enfermera:
    def __init__(self):
        self.a=''
            

    def menu_enfermera(self):
            while True:
                try:
                    opcionE = int(input("""1.Consultar informacion de citas\nIngrese una opción: """))

                    match opcionE:
                         case 1:
                              self.consulat_citas()
                         case __:
                              print('Pon el numero correcto.')
                      
                      
                except Exception as a:
                    print(f'Error en el menu de enfermera/o')
    
    def consulat_citas(self):
         citas1=citas()
         citas1.consultar_citas()
    def conslurtar_paciente():
        mascota1=Mascota()
        mascota1.consultar_mascota()
         
         