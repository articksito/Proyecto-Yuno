class Enfermera:
    def __init__(self):
        while True:
            print("\n\tBienvenido al menú de enfermera")
            print("Seleccione el apartado que desea consultar")
            print("\n1. Citas")
            print("2. Pacientes")
            print("3. Inventario de medicamentos")
            print("4. Citas próximas")
            print("5. Perfil de usuario")
            print("6. Salir")
            opcionE = input("Ingrese una opción: ")

            if opcionE == "1":
                while True:
                    print("\nHas ingresado al apartado de citas")
                    print("Ingresa la opción que deseas realizar:")
                    print("\n1. Consultar información de citas")
                    print("2. Registro de pacientes")
                    print("3. Historial de paciente")
                    print("4. Salir")
                    sub_opcion = input("Ingrese una opción: ")

                    if sub_opcion == "1":
                        print("Consultando información de citas...")
                    elif sub_opcion == "2":
                        print("Registrando nuevo paciente...")
                    elif sub_opcion == "3":
                        print("Mostrando historial del paciente...")
                    elif sub_opcion == "4":
                        print("Saliendo del apartado de citas...")
                        break
                    else:
                        print("Opción no válida, intente de nuevo.")

            elif opcionE == "2":
                while True:
                    print("\nHas ingresado al apartado de pacientes")
                    print("Ingresa la opción que deseas realizar:")
                    print("\n1. Lista de pacientes por tratar")
                    print("2. Modificar diagnóstico")
                    print("3. Modificar historial")
                    print("4. Observaciones")
                    print("5. Modificar receta")
                    print("6. Fecha de citas asignadas")
                    print("7. Salir")
                    sub_opcion = input("Ingrese una opción: ")

                    if sub_opcion == "1":
                        print("Mostrando lista de pacientes por tratar...")
                    elif sub_opcion == "2":
                        print("Modificando diagnóstico...")
                    elif sub_opcion == "3":
                        print("Modificando historial del paciente...")
                    elif sub_opcion == "4":
                        print("Agregando observaciones...")
                    elif sub_opcion == "5":
                        print("Modificando receta médica...")
                    elif sub_opcion == "6":
                        print("Consultando fechas de citas asignadas...")
                    elif sub_opcion == "7":
                        print("Saliendo del apartado de pacientes...")
                        break
                    else:
                        print("Opción no válida, intente de nuevo.")

            elif opcionE == "3":
                while True:
                    print("\nHas ingresado al apartado de inventario de medicamentos")
                    print("Ingresa la opción que deseas realizar:")
                    print("\n1. Registrar uso del medicamento")
                    print("2. Observaciones o notas")
                    print("3. Chequeo de inventario")
                    print("4. Salir")
                    sub_opcion = input("Ingrese una opción: ")

                    if sub_opcion == "1":
                        print("Registrando uso del medicamento...")
                    elif sub_opcion == "2":
                        print("Agregando observaciones al inventario...")
                    elif sub_opcion == "3":
                        print("Chequeando inventario...")
                    elif sub_opcion == "4":
                        print("Saliendo del apartado de inventario...")
                        break
                    else:
                        print("Opción no válida, intente de nuevo.")

            elif opcionE == "4":
                while True:
                    print("\nHas ingresado al apartado de citas próximas")
                    print("Ingresa la opción que deseas realizar:")
                    print("\n1. Lista de pacientes (citas próximas)")
                    print("2. Observaciones o notas")
                    print("3. Salir")
                    sub_opcion = input("Ingrese una opción: ")

                    if sub_opcion == "1":
                        print("Mostrando lista de pacientes con citas próximas...")
                    elif sub_opcion == "2":
                        print("Agregando observaciones a citas próximas...")
                    elif sub_opcion == "3":
                        print("Saliendo del apartado de citas próximas...")
                        break
                    else:
                        print("Opción no válida, intente de nuevo.")

            elif opcionE == "5":
                while True:
                    print("\nHas ingresado a la configuración de usuario")
                    print("Ingresa la opción que deseas realizar:")
                    print("\n1. Ver perfil")
                    print("2. Cambiar contraseña")
                    print("3. Cerrar sesión")
                    print("4. Salir")
                    sub_opcion = input("Ingrese una opción: ")

                    if sub_opcion == "1":
                        print("Mostrando perfil del usuario...")
                    elif sub_opcion == "2":
                        print("Cambiando contraseña...")
                    elif sub_opcion == "3":
                        print("Cerrando sesión...")
                    elif sub_opcion == "4":
                        print("Saliendo del perfil de usuario...")
                        break
                    else:
                        print("Opción no válida, intente de nuevo.")

            elif opcionE == "6":
                print("Saliendo del sistema... ¡Hasta pronto!")
                break

            else:
                print("Opción no válida, intente de nuevo.")