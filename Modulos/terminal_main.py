from terminal_recepcionista import *
from db_connection import *
from terminal_administrador import *
from terminal_enfermera import *
from terminal_veterinario import *
connetion_main=Conexion()

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
            else:
                print('Contraseña incorrecta')
        except Exception as a:
            print(f'Error en menu main:{a}')
        finally:
            connetion_main.limpiar_terminal()
        
        salir=input('Quieres salir?')

        if salir=='si':
            connetion_main.cerrar_conexion()
            break
            
    
main()
        
        
