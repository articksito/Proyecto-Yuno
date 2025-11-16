from db_connection import *
from cita import *

class Usuario:
    def __init__(self):
        self.conexion=Conexion()

    def menu_usuario(self):
        while True:
            try:
                opcion=int(input('''
                                    1.Registrar usuario
                                    2.Consultar usuarios
                                    3.Salir
                                    Elige:'''))
                match opcion:
                    case 1:
                        self.registro_usuario()
                    case 2:
                        self.consultar_usuarios()
                    case 3:
                        break
                    case __:
                        print(f'Pon un numero correcto')
            except Exception as a:
                print(f'Error en el menu de usuario: {a}')
    
    def registro_usuario(self):
        try:
            nombre=input('Nombre del usuario:')
            apellido=input('Apellido del usuario:')
            correo=input('Correo del usuario:')
            telefono=int(input('Telefono del usuario:'))
            contraseña=input('Contraseña del usuario:')
            status=input('Estatus del usuario(True or False):')
            rol=input('Rol del usuario:')
            
            datos=(nombre,apellido,correo,telefono,contraseña,status,rol)
            columnas=('nombre','apellido','correo','telefono','contraseña','status','rol')
            table='usuario'

            self.conexion.insertar_datos(table,datos,columnas)

        except Exception as a:
            print(f'Error al crear usuario: {a}')

    def consultar_usuarios(self):
        try:
            columnas=self.conexion.Select_users(table='usuario')
            for colum in columnas:
                print('\t'.join(map(str,colum)))

        except Exception as a:
            print (f'Error al consultar tablas de usuario: {a}')

                
    def consultrar_expediente(self):
        pass