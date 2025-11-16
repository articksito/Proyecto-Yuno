from cliente import *
from cita import *
from mascota import *

class Recepcionista:
    def __init__(self):
        self.nosense=''
    def menu_recepcion(self):
        while True:
            try:
                selccion=int(input('Selecciona\n1.Citas\n2.Clientes\n3.Mascotas\n4.Salir\nElige:'))
    
                match selccion :
                    case 1:
                        self.citas()
                    case 2:
                        self.cliente()
                    case 3:
                        self.mascota()
                    case 4:
                        break
            except Exception as a:
                print(f'Error en menu de recepcionista: {a}')

    def citas(self):
        cita1=citas()
        cita1.menu_citas()

    def cliente(self):
        cliente1=cliente()
        cliente1.mini_main()

    def mascota(self):
        mascota1=Mascota()
        mascota1.menu_mascotas()


