class Mascota:
    #No llame a la superclase porque no son necesarios todos los datos.
    def __init__ (self, id_mascota, nombre, especie,raza,edad, propietario):
        self.id_mascota=id_mascota
        self.nombre=nombre 
        self.especie=especie 
        self.raza=raza 
        self.edad=edad
        self.propietario=propietario 