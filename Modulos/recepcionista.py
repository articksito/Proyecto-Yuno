from cliente import *
from cita import *
from mascota import *
from veterinario import *

class Recepcionista:
    def __init__(self):
        self.cliente=cliente()
        self.veterinario=Veterinario()
        self.mascota=Mascota()
        self.cita=citas()

    def menu_recepcion(self):
        while True:
            try:
                selccion=int(input('Selecciona\n1.Citas\n2.Clientes\n3.Mascotas\n4.Ver veterinarios\n5.Salir\nElige:'))
    
                match selccion :
                    case 1:
                        self.cita.menu_citas()
                    case 2:
                        self.cliente.mini_main()
                    case 3:
                        self.mascota.menu_mascotas()
                    case 4:
                        self.veterinario.consultar_veterinarios()
                    case 5:
                        break
                    
            except Exception as a:
                print(f'Error en menu de recepcionista: {a}')


