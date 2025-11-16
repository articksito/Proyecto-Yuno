from usuario import *
from cita import *
from cliente import *
from mascota import *

class administrador:
    def menu_administrador(self):
        while True:
            try:
                opcion=int(input('''
                                    1.Usuario
                                    2.Mascota
                                    3.Cita
                                    4.Cliente
                                    5.Salir
                                    Elige:'''))
                
                match opcion:
                    case 1:
                        self.usuario()
                    case 2:
                        self.mascota()
                    case 3:
                        self.cita()
                    case 4:
                        self.cliente()
                    case 5:
                        break
                    case __:
                        print('Pon un numero correcto.')
            except Exception as a:
                print(f'Error en el menu de admin: {a}')
        pass
    def usuario(self):
        usuario1=Usuario()
        usuario1.menu_usuario()
    def mascota(self):
        mascota1=Mascota()
        mascota1.menu_mascotas()
    def cita(self):
        cita1=citas()
        cita1.menu_citas()
    def cliente(self):
        cliente1=cliente()
        cliente1.mini_main()
