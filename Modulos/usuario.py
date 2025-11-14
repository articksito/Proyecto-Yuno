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