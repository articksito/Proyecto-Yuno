from recepcionista import *
from db_connection import *
from administrador import *
connetion_main=Conexion()

def main():
    #Esto no va a ir aqui, solo es una prueba:v
    recepcion=Recepcionista()
    administrador1=administrador()
    selccion=int(input('Selecciona\n1.Recepcionista\n2.Administrador\nElige:'))
    
    match selccion :
        case 1:
            recepcion.menu_recepcion()
        case 2:
            administrador1.menu_administrador()
    
    connetion_main.cerrar_conexion()

   

main()
        
        
