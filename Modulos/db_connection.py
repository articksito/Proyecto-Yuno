import psycopg2
from psycopg2 import sql

class Conexion:
    def __init__(self):
        self.conexion1 = psycopg2.connect("postgresql://neondb_owner:npg_M1nvy9aksESm@ep-raspy-star-afucb7a1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
        self.cursor_uno = self.conexion1.cursor()

    def insertar_datos(self,sql:str,datos:tuple=None):
        self.cursor_uno.execute(sql,datos)
        self.conexion1.commit()
        self.cursor_uno.close()

    def Select_users(self,table:str):
        try:
            code = sql.SQL("SELECT * FROM {} ").format(sql.Identifier(table))
            self.cursor_uno.execute(code)
            table=self.cursor_uno.fetchall()
            return table
        except:
            print("Error")

        self.cursor_uno.close()

    def Validacion_usuario(self, id_user: int):
        self.id_user = id_user
        self.validacion = bool

        sql = "SELECT 1 FROM usuario where id_usuario = %s"

        self.cursor_uno.execute(sql, (id_user,))
        result = self.cursor_uno.fetchone()

        self.validacion = result is not None

        return self.validacion

    def Validacion_contrasena(self, user_pwd):
        self.pwd = user_pwd
        self.validacion_pwd = bool

        sql = "SELECT contraseña FROM usuario WHERE id_usuario = %s"
        
        self.cursor_uno.execute(sql, (self.id_user,))

        for row in self.cursor_uno:
            if row[0]== self.pwd:
                self.validacion_pwd = True
            else:
                self.validacion_pwd = False
        
        return self.validacion_pwd 