from db_connection import Conexion
# checa jose, why ya hay otro usuario, es validacion? se supone que yo hacia el user no? que se supone que debo agregar?
class Usuario:
    def __init__(self):
        self.conexion = Conexion()

    def menu_usuario(self):
        while True:
            try:
                opcion = int(input('''
==============================
        MENÚ USUARIO
==============================
1. Registrar usuario
2. Consultar usuarios
3. Modificar usuario
4. Eliminar usuario
0. Salir
==============================
Selecciona una opción: '''))

                if opcion == 1:
                    self.registrar_usuario()
                elif opcion == 2:
                    self.consultar_usuario()
                elif opcion == 3:
                    self.modificar_usuario()
                elif opcion == 4:
                    self.eliminar_usuario()
                elif opcion == 0:
                    return
                else:
                    print(" xd")

            except Exception as e:
                print(f" Hola Jose: {e}")

    
    def registrar_usuario(self):
        try:
            id_usuario = input("ID del usuario: ")
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            correo = input("Correo: ")
            telefono = input("Teléfono: ")
            contrasena = input("Contraseña: ")
            status = input("Status (activo o inactivo): ")

            datos = {
                "id_usuario": id_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "telefono": telefono,
                "contrasena": contrasena,
                "status": status
            }

            self.conexion.insertar_datos("usuario", datos)
            print(" Usuario registrado ")

        except Exception as e:
            print(f" Error: {e}")

    def consultar_usuario(self):
        
            print(" LISTA DE USUARIOS ")
            self.conexion.selcionar_dato("usuario")



    def modificar_usuario(self):
        try:
            id_usuario = input("ID del usuario a modificar: ")
            datos = {}
            columna = input("Nombre de la columna a modificar: ")
            valor = input(f"Nuevo valor para {columna}: ")

            datos[columna] = valor

            self.conexion.editar_registro(
                id_usuario,
                datos,
                tabla="usuario",
                id_columna="id_usuario"
            )

            print(" Usuario modificado.")

        except Exception as e:
            print(f" Error: {e}")


    def eliminar_usuario(self):
        id_usuario = input("ID del usuario a eliminar: ")

        self.conexion.eliminar_registro(
             "usuario",
             id_usuario,
            "id_usuario"
            )
        print(" Usuario eliminado")
