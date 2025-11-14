class citas:
    def menu_citas():
        while True:
            print("Bienvenido al menu de citas")
            print("Elige una opcion: ")
            print("")
            print("1. Editar citas")
            print("2. Revisar las citas")
            print("3. Ver expedientes")
            print("4. Confirmar las citas")
            print("5. Crear citas de rutina")
            print("6. Ver citas del dia")
            print("7. Salir")
            
            try:
                opcionC = int(input("Elije la opcion que desees elegir (1-7): "))
            except ValueError:
                print("Error: Debe ingresar un número válido")
                continue
            
            match opcionC:
                case 1:
                    print("Has elegido el editor de citas")
                case 2:
                    print("Estas revisando las citas")
                case 3:
                    print("Estas mirando los expedientes")
                case 4:
                    print("Has entrado a la confirmacion de citas")
                case 5:
                    print("Estas ceando citas de rutina")
                case 6:
                    print("Estas viendo las citas del dia de hoy")
                case 7:
                    print("Buen dia")
                    break
                case _:
                    print("Elige una opcion del 1 al 7")
                
                