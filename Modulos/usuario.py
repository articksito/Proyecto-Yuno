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
3.Modificar usuarios
4.Eliminar usuario
5.Salir
Elige:'''))
                match opcion:
                    case 1:
                        self.registro_usuario()
                    case 2:
                        self.consultar_usuarios()
                    case 3:
                        self.modificar_usuarios()
                    case 4:
                        self.eliminar_usuario()
                    case 5:
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

            seleccion_rol=int(input('''Seleccion de rol.\n1.Recepcionista
2.Enfermera/o\n3.Veterinario\n4.Admin\nElige: '''))
            rol=''
            
            while seleccion_rol:
                try:
                    match seleccion_rol:
                        case 1:
                            rol='Recepcionista'
                            seleccion_rol=False
                        case 2:
                            rol='Enfermera/o'
                            seleccion_rol=False
                        case 3:
                            rol='Veterinario'
                            seleccion_rol=False
                        case 4:
                            rol='Admin'
                            seleccion_rol=False
                        case __:
                            print('Pon el numero correcto')
                except:
                    print("Pon caracteres validos")

            
            datos=(nombre,apellido,correo,telefono,contraseña,status,rol)
            columnas=('nombre','apellido','correo','telefono','contraseña','status','rol')
            table='usuario'
            print(datos)

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
    
    def modificar_usuarios(self):
        try:
            datos={}
            id=int(input('ID:'))  

            while True:
                columna=input('Nombre de la columuna:').strip()
                valor=input(f'nuevo valor({columna}):')

                datos[columna]=valor

                cerrar=int(input('Son todos? (1 para si)'))
                if cerrar==1:
                    break 

            self.conexion.editar_registro(id,datos,tabla='usuario',id_columna='id_usuario')

        except Exception as a:
            print(f'Error al modificar usuario: {a}')

    def eliminar_usuario(self):
        try:
            id=int(input('Id del usuario a eliminar:'))
            self.conexion.eliminar_registro(id,tabla='usuario',id_columna='id_usuario')

        except Exception as a:
            print(f'Error al eliminar usuario desde usuario: {a}')
              
    def consultrar_expediente(self):
        pass