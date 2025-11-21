from recepcionista import *
from db_connection import *
from administrador import *
from enfermera import *
from veterinario import *
connetion_main=Conexion()

def main():
    #Esto no va a ir aqui, solo es una prueba:v
    recepcion=Recepcionista()
    administrador1=administrador()
    veterinario=Veterinario()
    enfermera=Enfermera()

  
    
    while True:
        try:
            selccion=int(input('''Selecciona\n1.Recepcionista\n2.Administrador
3.Enfermero/a\n4.Veterinario\n5.Salir\nElige:'''))
            
            match selccion :
                case 1:
                    recepcion.menu_recepcion()
                    connetion_main.limpiar_terminal()
                case 2:
                    administrador1.menu_administrador()
                    connetion_main.limpiar_terminal()
                case 3:
                    enfermera.menu_enfermera()
                    connetion_main.limpiar_terminal()
                case 4:
                    veterinario.menu_veterinario()
                    connetion_main.limpiar_terminal()
                case 5:
                    break
        except Exception as a:
            print(f'Error en menu main:{a}')

            
    connetion_main.cerrar_conexion()

main()
        
        
