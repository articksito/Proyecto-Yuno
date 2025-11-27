from terminal_recepcionista import *
from db_connection import *
from terminal_administrador import *
from Modulos.Version_terminal.terminal_enfermera import *
from terminal_veterinario import *
connetion_main=Conexion()
import sys
import os
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
carpeta_padre = os.path.dirname(carpeta_actual)
sys.path.append(carpeta_padre)


def main():
    recepcion=Recepcionista()
    administrador1=administrador()
    veterinario=Veterinario()
    enfermera=Enfermera()
    
    while True:
        try:
            id_usuario=input('ID:')
            contraseña=input('Contraseña:')

            validacion_user=connetion_main.Validacion_usuario(id_usuario)
            validacion_contraseña=connetion_main.Validacion_contrasena(contraseña)
            rol=connetion_main.Validacion_Perfil(id_usuario)
            
            if validacion_user and validacion_contraseña:
            
                match rol :
                    case 'REP':
                        recepcion.menu_recepcion() 
                    case 'ADMIN':
                        administrador1.menu_administrador()
                    case 'ENF':
                        enfermera.menu_enfermera()
                    case 'VET':
                        veterinario.menu_veterinario()
                    case __:
                        print('Rol no existeX2 ')
                        input('Dale Enter')

            else:
                print('Contraseña incorrecta')
                input('Dale Enter')

        except Exception as a:
            print(f'Error en menu main:{a}')
            input('Dale Enter')

        finally:
            connetion_main.limpiar_terminal()
        
            salir=input('Quieres salir?')
            if salir=='si':
                connetion_main.cerrar_conexion()
                break
            
    
main()
        
        
