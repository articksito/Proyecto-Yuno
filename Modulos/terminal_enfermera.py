from terminal_cita import *
from db_connection import *
from terminal_mascota import *


class Enfermera:
    def __init__(self):
        self.conexion=Conexion()
            

    def menu_enfermera(self):
            while True:
                try:
                    opcionE = int(input("""1.Consultar informacion de citas\n2.Consultar imformancion de pacientes
3.Actualizar diagnostico\n4.Cambiar contraseña\n5.Agregar medicina a farmacia\n6.Consultar medicina\n7.Internar mascota
8.Salir\nIngrese una opción: """))

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
                        case 6:
                              self.consultar_medicamento()
                        case 7:
                            self.internar()
                        case 8:
                            break
                        case __:
                              print('Pon el numero correcto.')
                              input('Dale Enter')
                      
                except Exception as a:
                    print(f'Error en el menu de enfermera/o')
                    input('Dale Enter')
                finally:
                    self.conexion.limpiar_terminal()
    
    def consulat_citas(self):
         citas1=citas()
         citas1.consultar_citas()
    def consultar_paciente():
        mascota1=Mascota()
        mascota1.consultar_mascota()

    def actualizar_diagnostico(self):
        self.conexion.limpiar_terminal()
        ruta_expediente='/home/owner_jose/Proyecto-Yuno/diagnostico.txt'
        comando_expediente=input('Agrega algo:')
        with open(ruta_expediente, 'a') as f:
            f.write(comando_expediente)
        input('Dale Enter')

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
            input('Dale Enter')

        except Exception as a:
             print(f'Error al agregar medicina: {a}')
             input('Dale Enter')

        finally:
            self.conexion.limpiar_terminal()
    
    def consultar_medicamento(self):
        try:
            columnas=self.conexion.Select_users(table='medicamento')
            for colum in columnas:
                print('\t'.join(map(str,colum)))
            input('Dale Enter')

        except Exception as a:
            print (f'Error al consultar medicamentos en repertorio: {a}')
            input('Dale Enter')

        finally:
            self.conexion.limpiar_terminal()
        
    def internar(self):
            try:
                observaciones=input('Pon las observaciones:')
                id_consulta=int(input('Pon el id de consultar:'))

                datos=(observaciones,id_consulta)
                columnas=('observaciones','fk_consulta')
                table='hospitalizacion'
                
                self.conexion.insertar_datos(table,datos,columnas)
                input('Dale Enter')

            except Exception as a:
                print(f'Error al internar:{a}')
                input('Dale Enter')
                
            finally:
                self.conexion.limpiar_terminal()
