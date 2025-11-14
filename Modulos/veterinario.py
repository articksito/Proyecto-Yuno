class Veterinario:
    def menuVET():
        while True:
            print("------Bienvenido al menu de veterinario------")
            print("Seleccione que es lo que quiere realizar")
            print("1. Buscar paciente")
            print("2. Mirar los proximos pacientes")
            print("3. Cerrar sesion")

            try:
                opcionVET = int(input("Ingresa la opcion que deseas seleecionar (1-3): "))
            except ValueError:
                print("Error: Debe ingresar un número válido")
                continue
            while True:
                match opcionVET:
                    case 1:
                        print("---Buscando paciente---")
                        print("Seleccione que desea realizar")
                        print("")
                        print("Ingresa la id del paciente que desees buscar")
                        print(f"Ingresa 0 (cero) para cancelar")
                
                        try:
                            idcheck = int(input("Ingresa lo requerido"))
                        except ValueError:
                            print("Error: Debe ingresar un número válido")
                            continue
                        
                        if idcheck == 0:
                            print("Regresando al menu de veterinario")
                            break
                        elif idcheck == id:
                            #! mostrar todo lo de la mascota
                            while True:
                                print("Elige la opcion que quieres realizar")
                                print("")
                                print("1. Ver expediente completo")
                                print("2. Modificar expediente")
                                print("3. Regresar al menu")
                                
                                try:
                                    opcion1 = int(input("Ingresa la accion necesaria"))
                                except ValueError:
                                    print("Error: Debe ingresar un número válido")
                                    continue
                            
                                match opcion1:
                                    case 1:
                                        print("Motrando expediente completo") #!--------------------------
                                    case 2:
                                        print("Configurando expediente") #!--------------------------
                                    case 3:
                                        print("Regresando al menu") #!--------------------------
                                        break
                        else:
                            print("Ingresa una id valida")
           
                    case 2:
                        print("Mostrando los pacientes que siguen") #!--------------------------
                        #* Aqui se liga con la base de datos
                        try:
                            opcion2 = int(input("Ingresa 0 (cero) para volver al menu "))
                        except ValueError:
                            print("Error: Debe ingresar un número válido")
                            continue
                        if opcion2 == 0:
                            print("Regresando al menu...")
                            break
                        else:
                            print("Opcion invalida, ingresa una opcion valida")
                        
                    case 3:
                        print("Regresando al menu principal")
                        break
                                    