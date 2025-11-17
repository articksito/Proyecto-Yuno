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

    selccion=int(input('''Selecciona\n1.Recepcionista\n2.Administrador
3.Enfermero/a\n4.Veterinario\nElige:'''))
    
    match selccion :
        case 1:
            recepcion.menu_recepcion()
        case 2:
            administrador1.menu_administrador()
        case 3:
            enfermera.menu_enfermera()
        case 4:
            veterinario.menu_veterinario()

            
    connetion_main.cerrar_conexion()

main()
        
        
