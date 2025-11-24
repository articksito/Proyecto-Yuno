from db_connection import *

class citas:
    def __init__(self):
        self.conexion1=Conexion()
        
    def menu_citas(self):
        print("Bienvenido al menu de citas")
        while True:
            try:    
                    print("""1. Crear cita"\n2. Editar las citas\n3.Eliminar cita\n4.Consultar citas\n5.Buscador de citas
6.Salir""")
                    opcionC = int(input("Elije la opcion que desees elegir: "))
                    match opcionC:
                        case 1:
                            self.crear_cita()
                        case 2:
                            self.modificar_cita()
                        case 3:
                            self.eliminar_cita()
                        case 4:
                            self.consultar_citas()
                        case 5:
                            self.buscardor_de_citas()
                        case 6:
                            break
            except ValueError:
                    print("Error: Debe ingresar un número válido")
                    input('Dale Enter')

            finally:
                self.conexion1.limpiar_terminal()
                     
                
    def crear_cita(self):
        try:
            fecha=input('Pon la fecha:')
            hora=input('Pon hora:')
            estado=input('El estado del animal:')
            motivo=input('Motivo:')
            mascota=int(input('Id de mascota:'))
            veterinario=int(input('Id de veterinario:'))
            
            datos=(fecha,hora,estado,motivo,mascota,veterinario)
            columnas=('fecha','hora','estado','motivo','fk_mascota','fk_veterinario')
            table='cita'

            self.conexion1.insertar_datos(table,datos,columnas)
            input('Dale Enter')

        except Exception as a:
            print(f'Error al crear cita: {a}')
            input('Dale Enter')

        finally:
            self.conexion1.limpiar_terminal()

    def modificar_cita(self):
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

            self.conexion1.editar_registro(id,datos,tabla='cita',id_columna='id_cita')
            input('Dale Enter')

        except Exception as a:
            print(f'Error al modificar cita: {a}')
            input('Dale Enter')

        finally:
            self.conexion1.limpiar_terminal()
    
    def eliminar_cita(self):
        try:
            id=int(input('Id de la cita a eliminar:'))
            self.conexion1.eliminar_registro(id,tabla='cita',id_columna='id_cita')
            input('Dale Enter')

        except Exception as a:
            print(f'Error al eliminar cita: {a}')
            input('Dale Enter')

        finally:
            self.conexion1.limpiar_terminal()
                
    def consultar_citas(self):
        try:
            columnas=self.conexion1.Select_users(table='cita')
            for colum in columnas:
                print('\t'.join(map(str,colum)))
            input('Dale Enter')

        except Exception as a:
            print (f'Error al consultar citas: {a}')
            input('Dale Enter')

        finally:
            self.conexion1.limpiar_terminal()
            
    def buscardor_de_citas(self):
        print (" BUSCADOR DE CITAS ")
        while True:
            try:
                opcion= int (input('''
    1. Buscar cita por ID
    2. Buscar cita por de Mascota
    3. Buscar cita por ID Cliente
    4. Buscar cita por ID Veterinario
    5. Salir
    Por cual metodo seas realizar la busqueda : '''))
                if opcion ==5:
                    break
                
                buscador= input('Ingresa el dato para la busqueda : ')
                resultados = []
                columna_busqueda = ''
                
                match opcion: 
                    case 1: #este es de id de cita
                        columna_busqueda='id_cita'
                        resultados= self.conexion1.select_con_filtro('cita', columna_busqueda, buscador)
                    
                    case 2: #Por nombre de mascota
                        columna_busqueda= 'fk_mascota'
                        resultados= self.conexion1.select_con_filtro('cita', columna_busqueda,buscador)
                    case 3:
                        continue
                    case 4: 
                        columna_busqueda='fk_veterinario'
                        resultados= self.conexion1.select_con_filtro('cita',columna_busqueda, buscador)
                    case __:
                        print('opcion no valida')
                        continue
                if resultados:
                    print(f"\n--- Resultados para '{buscador} en {columna_busqueda}---'")
                    input()

                    for i in resultados:
                        print(f"ID: {i[0]} \n FECHA: {i[1]} \n HORA: {i[2]} \n ESTADO {i[3]}\n ID MASCOTA: {i[5]}\n ID VETERINARIO ASIGNADO: {i[6]}")
                    input()
                else:
                    print(" No se encontro ninguna cita con ese valor")
                input('Dale Enter')

            except ValueError:
                print ("Error: Ingresar solo numeros")
                input('Dale Enter')

            except Exception as e:
                print(f" Error con el buscador: {e}")
                input('Dale Enter')
                
            finally:
                self.conexion1.limpiar_terminal()
                
                
                    
                    
            
                    
                    
                        
                        
                        
                
                
                
                