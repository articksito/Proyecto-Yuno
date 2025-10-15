class Registro:
# Datos Generales - Si los cambian avisen y comenten 
    def __init__(self, id_registro, nombre, historial, comentarios):
        self.id_registro=id_registro
        self.nombre=nombre
        self.historial= historial
        self.comentarios=comentarios 
        
class Mascota:
    #No llame a la superclase porque no son necesarios todos los datos.
    def __init__ (self, id_mascota, nombre, especie,raza,edad, propietario):
        self.id_mascota=id_mascota
        self.nombre=nombre 
        self.especie=especie 
        self.raza=raza 
        self.edad=edad
        self.propietario=propietario 
        
class Usuario:
    def __init__(self,matricula,nombre,telefono):
        self.matricula=matricula
        self.nombre=nombre 
        self.telefono=telefono
        self.mascotas= [] #Por si va a registrar mas mascotas 
    
    def registro_mascota(self,mascota):
        self.mascotas.append(mascota)
        print(f"La mascosta {self.nombre} fue registrada con exito ")
        
    def consultrar_expediente(self):
        pass

class Veterinario:
    def __init__(self,clave,nombre,especialidad):
        self.clave=clave
        self.nombre=nombre
        self.especialidad=especialidad 
        
    def autenticacion(self):
        ######AQUI ES DONDE SE MANDARA AL SELECCIONAR EL MENU DE VETERINARIO Y SI SE LOGUEA BIEN SE MANDA AL MENU########
        pass
        
    def menu(self):
        while True:
            print("\n\tBienvenido al menu de veterinario")
            print("\n1. Consultar expediente")
            print("\n2. Añadir comentarios")
            print("\n3. Ver pacientes en tratamiento")
            print("\n4. Agregar pacientes")
            print("\n5. Dar de alta")
            print("\n6. Dar de baja")
            print("\n7. ")
            print("\n8. ")
            print("\n9. ")
            print("\n10. Salir")
            opcionV = input()
            
            if opcionV == 1:
                pass
            elif opcionV == 2:
                pass
            elif opcionV == 3:
                pass
            elif opcionV == 4:
                pass
            elif opcionV == 5:
                pass
            elif opcionV == 6:
                pass
            elif opcionV == 7:
                pass
            elif opcionV == 8:
                pass
            elif opcionV == 9:
                pass
            elif opcionV == 10:
                print("Regresando al menu principal")
                break                
            else:
                print("Opcion invalida")
        
    def consultar_expediente(self):
        pass
        
    def añadir_comentarios (self):
        pass 

class Recepcionista:
    def __init__(self,clave,nombre):
        pass
    def agendar_citas(self):
        pass
    def ver_registros(self):
        pass

class Admin:
    pass

def main():
    pass
main()
        
        
