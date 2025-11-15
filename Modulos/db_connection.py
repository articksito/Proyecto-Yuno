import psycopg2
from psycopg2 import sql

class Conexion:
    def __init__(self):
        self.conexion1 = psycopg2.connect("postgresql://neondb_owner:npg_M1nvy9aksESm@ep-raspy-star-afucb7a1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
        self.cursor_uno = self.conexion1.cursor()

    def insertar_datos(self,table:str,datos:tuple=None,columna:tuple=None):
        try:
            columas_safe=[sql.Identifier(c) for c in columna] #Use la compresion de Barac :v
            lugares=[sql.SQL('%s')]*len(datos)

            comando=sql.SQL('INSERT INTO {}({}) VALUES ({})').format(sql.Identifier(table),sql.SQL(', ').join(columas_safe), sql.SQL(', ').join(lugares))
            self.cursor_uno.execute(comando,datos)
            self.conexion1.commit()

            print("Correcto")
        except psycopg2.Error as error:
            print(f"Error en insertar_datos: {error}")
            self.conexion1.rollback()


    def Select_users(self,table:str):
        try:
            code = sql.SQL("SELECT * FROM {} ").format(sql.Identifier(table))
            self.cursor_uno.execute(code)
            table=self.cursor_uno.fetchall()
            return table
        except Exception as a:
            print(f"Error en Select_users:{a}")

    def editar_registro(self,id:int,datos:dict,tabla:str,id_columna:str):
        try:
            comando=[]
            valores=[]

            for columna, valor in datos.items():
                comando.append(sql.SQL("{}=%s").format(sql.Identifier(columna)))
                valores.append(valor)

            unir=sql.SQL(', ').join(comando)

            comando_sql= sql.SQL("""
                                 UPDATE {}
                                 SET {}
                                 WHERE {}=%s
                                 """).format(sql.Identifier(tabla),unir, sql.Identifier(id_columna))
            
            valores.append(id)

            self.cursor_uno.execute(comando_sql,tuple(valores))
            self.conexion1.commit()
            print('Correcto')
        except Exception as a:
            print(f"Error al editar registro/s:{a}")

    def cerrar_conexion(self):
        if self.conexion1:
            self.conexion1.close()
        if self.cursor_uno:
            self.cursor_uno.close
        print('Cerrado, vuelva pronto')


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