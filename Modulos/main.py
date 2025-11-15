from recepcionista import *
from db_connection import *
connetion_main=Conexion()

def main():
    recepcion=Recepcionista()
    selccion=int(input('Selecciona\n1.Cliente\n2.Cita\n'))
    
    match selccion :
        case 1:
            recepcion.cliente()
        case 2:
            recepcion.citas()
    

    connetion_main.cerrar_conexion()

   

main()
        
        
