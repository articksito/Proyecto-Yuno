from usuario import *
from cita import *
from cliente import *
from mascota import *
from db_connection import *

class administrador:
    def __init__(self):
        self.conexion=Conexion()

    def menu_administrador(self):
        while True:
            try:
                opcion=int(input('''
                                    1.Usuario
                                    2.Mascota
                                    3.Cita
                                    4.Cliente
                                    5.Eliminar records de tabla entera.
                                    6.Salir
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
                        self.eliminar_datos_full()
                    case 6:
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

    def eliminar_datos_full(self):
        while True:
            try:
                opcion_tabla=int(input('''Tabla a eliminar\n1.Cita\n2.Cliente\n3.Mascota\n4.Usuario
5.Consulta\n6.Enfermero\n7.Especialidad\n8.Hospitalizacion\n9.Medicamento\n10.Receta
11.Receta a medicamento\n12.Tipo de animal\n13.Veterinario\n14.Salir\nElige:  '''))                    
                
                match opcion_tabla:
                    case 1:
                        tabla='cita'
                    case 2:
                        tabla='cliente'
                    case 3:
                        tabla='mascota'
                    case 4:
                        tabla='usuario'
                    case 5:
                        tabla='consulta'
                    case 6:
                        tabla='enfermero'
                    case 7:
                        tabla='especialidad'
                    case 8:
                        tabla='hospitalizacion'
                    case 9:
                        tabla='medicamento'
                    case 10:
                        tabla='receta'
                    case 11:
                        tabla='receta_medicamento'
                    case 12:
                        tabla='tipo_animal'
                    case 13:
                        tabla='veterinario'
                    case 14:
                        break
                    case __:
                            print('Pon numero valido')

                self.conexion.truncase(tabla)

            except Exception as a:
                print(f'Fallo desde administrador:{a}')