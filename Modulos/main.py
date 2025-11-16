from recepcionista import *
from db_connection import *
connetion_main=Conexion()

def main():
    #Esto no va a ir aqui, solo es una prueba:v
    recepcion=Recepcionista()
    selccion=int(input('Selecciona\n1.Recepcionista\n'))
    
    match selccion :
        case 1:
            recepcion.menu_recepcion()
        case 2:
            pass
    
    connetion_main.cerrar_conexion()

   

main()
        
        
