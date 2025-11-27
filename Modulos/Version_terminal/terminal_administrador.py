from terminal_usuario import *
from terminal_recepcionista import *
from terminal_veterinario import *
from Modulos.Version_terminal.terminal_enfermera import *
from db_connection import *
import sys
import os
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
carpeta_padre = os.path.dirname(carpeta_actual)
sys.path.append(carpeta_padre)

class administrador:
    def __init__(self):
        self.conexion=Conexion()
        self.recepcion=Recepcionista()
        self.veterinario=Veterinario()
        self.enfermera=Enfermera()
        self.usuario=Usuario()

    def menu_administrador(self):
        while True:        
            try:

                opcion=int(input('''
1.Usuario
2.Recepcion
3.Veterinario
4.Enfermero/a
5.Eliminar records de tabla entera.
6.Agregar algun tipo de animal
7.Consultar tipo de animal
8.Salir
Elige:'''))
                
                match opcion:
                    case 1:
                        self.usuario.menu_usuario()
                    case 2:
                        self.recepcion.menu_recepcion()
                    case 3:
                        self.veterinario.menu_veterinario()
                    case 4:
                        self.enfermera.menu_enfermera()
                    case 5:
                        self.eliminar_datos_full()
                    case 6:
                        self.agregar_tipo_animal()
                    case 7:
                        self.consulta_tipo_animal()
                    case 8:
                        break
                    case __:
                        print('Pon un numero correcto.')
                        input('Dale Enter')

            except Exception as a:
                print(f'Error en el menu de admin: {a}')
                input('Dale Enter')

            finally:
                self.conexion.limpiar_terminal()

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
                            input('Dale Enter')

                self.conexion.truncase(tabla)

            except Exception as a:
                print(f'Fallo desde administrador:{a}')
                input('Dale Enter')

            finally:
                self.conexion.limpiar_terminal()
        
    def agregar_tipo_animal(self):
        try:
            especie=input('Especie del animal:')
            raza=input('Raza del animal:')
            descripocion=input('Descripcion del animal:')
            
            
            datos=(especie,raza,descripocion)
            columnas=('especie','raza','descripcion')
            table='tipo_animal'

            self.conexion.insertar_datos(table,datos,columnas)
            input('Dale Enter')

        except Exception as a:
             print(f'Error al agregar tipo del animal: {a}')
             input('Dale Enter')

        finally:
            self.conexion.limpiar_terminal()

    def consulta_tipo_animal(self):
        self.conexion.limpiar_terminal()
        try:
            columnas=self.conexion.Select_users(table='tipo_animal')
            for colum in columnas:
                print('\t'.join(map(str,colum)))
            input('Dale Enter')

        except Exception as a:
            print (f'Error al consultar tipos de animales: {a}')
            input('Dale Enter')
            
        finally:
            self.conexion.limpiar_terminal()

'''
b=administrador()
b.agregar_tipo_animal
'''