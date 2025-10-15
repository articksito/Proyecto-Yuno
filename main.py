class Registro:
# Datos Generales - Si los cambian avisen y comenten 
    def __init__(self, id_registro, nombre, historial, comentarios):
        self.id_registro=id_registro
        self.nombre=nombre
        self.historial= historial
        self.comentarios=comentarios 
        vsyufuagfiugi
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
        
        
