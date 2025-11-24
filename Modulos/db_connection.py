import psycopg2
from psycopg2 import sql
import os

class Conexion:
    def __init__(self):
        self.conexion1 = psycopg2.connect("postgresql://neondb_owner:npg_M1nvy9aksESm@ep-raspy-star-afucb7a1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
        self.cursor_uno = self.conexion1.cursor()

    def truncase(self,table:str):
        try:
            code = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(sql.Identifier(table))

            self.cursor_uno.execute(code)
            self.conexion1.commit()

            print(f'{table} reiniciada')

        except Exception as a:
            print(f'Error en conxion: {a}')

            if hasattr(self, 'conexion'):
             self.conexion1.rollback()

    def select_con_filtro(self, table: str, condition_column: str, condition_value):
        try: #Ilike es para buscar nombres, y los %s son para los ids.
            buscador = sql.SQL("SELECT * FROM {} WHERE {} ILIKE %s").format(
                sql.Identifier(table),
                sql.Identifier(condition_column)
            )
            if condition_column.startswith('id_'):
                search_value= str(condition_value)
            else:
                search_value= f"%{condition_value}%"
            
            self.cursor_uno.execute(buscador, (search_value,))
            resultados= self.cursor_uno.fetchall()
            
            return resultados 
        except Exception as a:
            print(f'Error al seleccionar la busqueda')
            return []
    def select_citas_por_cliente(self, id_cliente):
        try:
            especial = """SELECT c.* FROM cita c JOIN mascota m ON c.fk_mascota = m.id_mascota WHERE m.fk_cliente = %s; """
            self.cursor_uno.execute(especial , (id_cliente,))
            return self.cursor_uno.fetchall()
            
        except Exception as e:
            print(f'Error al buscar citas por cliente: {e}')
            return []

    # --- NUEVA FUNCIÓN: CONSULTAR (SELECT) ---
    def consultar_registro(self, tabla:str, id_columna:str, id_valor, columnas=None):
        """
        Busca un registro por ID y retorna las columnas solicitadas.
        Si columnas=None, retorna SELECT * (cuidado con el orden).
        Retorna una tupla con los valores o None.
        """
        try:
            if columnas:
                cols_sql = sql.SQL(", ").join([sql.Identifier(c) for c in columnas])
            else:
                cols_sql = sql.SQL("*")

            query = sql.SQL("SELECT {} FROM {} WHERE {} = %s").format(
                cols_sql,
                sql.Identifier(tabla),
                sql.Identifier(id_columna)
            )

            self.cursor_uno.execute(query, (id_valor,))
            resultado = self.cursor_uno.fetchone()
            return resultado

        except Exception as e:
            print(f"Error en consultar_registro: {e}")
            raise e
    

    def insertar_datos(self,table:str,datos:tuple=None,columna:tuple=None):
        try:

            columas_safe=[sql.Identifier(c) for c in columna] #Use la compresion de Barac :v
            lugares=[sql.SQL('%s')]*len(datos)

            #devolver_id=int(input('Queires devolver el id?\n1.Para si\nElige:'))
            
            pk_columna = 'id_' + table

            comando=sql.SQL('INSERT INTO {}({}) VALUES ({}) RETURNING {}').format(sql.Identifier(table),sql.SQL(', ').join(columas_safe), sql.SQL(', ').join(lugares)
                ,sql.Identifier(pk_columna))
            
            self.cursor_uno.execute(comando,datos)
            id_generado = self.cursor_uno.fetchone()[0]
            print("Correcto")
            
            self.conexion1.commit() 
            return id_generado
            
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
        
    def selcionar_dato(self,dato:int,table:str,columna:str):
        try:
            comando_sql = sql.SQL("SELECT {} FROM {} WHERE {} = %s").format(
            sql.Identifier(columna),
            sql.Identifier(table),
            sql.Identifier(columna)
        )
            
            self.cursor_uno.execute(comando_sql,dato)
            a=self.cursor_uno.fetchone()

            return a[0]
        
        except Exception as a:
            print(f'Error al seleccionar dato:{a}')

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

    from psycopg2 import sql

    def update_registro(self, id, datos:dict, tabla:str, id_columna:str):

        if not datos:
            print("No se proporcionaron datos para actualizar.")
            return False

        try:
            # Crear asignaciones dinámicas "columna = %s"
            columnas = [sql.Identifier(col) for col in datos.keys()]
            asignaciones = [
                sql.SQL("{} = %s").format(col)
                for col in columnas
            ]

            # Construir SQL seguro
            query = sql.SQL("""
                UPDATE {tabla}
                SET {asignaciones}
                WHERE {id_columna} = %s
            """).format(
                tabla=sql.Identifier(tabla),
                asignaciones=sql.SQL(", ").join(asignaciones),
                id_columna=sql.Identifier(id_columna)
            )

            # Valores en el orden correcto (valores del dict + el ID al final para el WHERE)
            valores = list(datos.values()) + [id]

            # Ejecutar
            self.cursor_uno.execute(query, valores)
            self.conexion1.commit()

            print("Registro actualizado correctamente.")
            return True

        except Exception as e:
            self.conexion1.rollback()
            print(f"Error al editar registro: {e}")
            raise e # Relanzamos el error para mostrarlo en el QMessageBox de la UI


    def eliminar_registro(self,id:int,tabla:str,id_columna:str):
        try:

            comando_sql=sql.SQL("""
                        DELETE FROM {}
                        WHERE {}=%s
                                """).format(sql.Identifier(tabla),sql.Identifier(id_columna))
            self.cursor_uno.execute(comando_sql,(id,))
            self.conexion1.commit()
            print('Eliminado correctamente.')
        except Exception as a:
            print(f"Error al eliminar registro:{a}")
            self.conexion1.rollback()

    def cerrar_conexion(self):
        if self.conexion1:
            self.conexion1.close()
        if self.cursor_uno:
            self.cursor_uno.close
        print('Cerrado, vuelva pronto')

        #Verifica que exista el usuario
    def Validacion_usuario(self, id_user: int):
        self.id_user = id_user
        self.validacion = bool

        sql = "SELECT 1 FROM usuario WHERE id_usuario = %s"

        self.cursor_uno.execute(sql, (id_user,))
        result = self.cursor_uno.fetchone()

        self.validacion = result is not None

        return self.validacion

        #Devuelve el rol
    def Validacion_Perfil(self, perffil: int):
        self.perfil = perffil
        self.rol = ""

        self.cursor_uno.execute("SELECT rol FROM usuario WHERE id_usuario = %s", (perffil,))
        result= self.cursor_uno.fetchone()

        if result:
            rol = result[0]
            self.rol = rol
        else:
            print("Usuario no encontrado.")

        return self.rol

    #retorna el nombre del usuario
    def Nombre_Usuario (self, perffil: int):
        self.perfil = perffil
        self.nombre_usuario = ""
        self.apellido_usuario = ""

        self.cursor_uno.execute("SELECT nombre FROM usuario WHERE id_usuario = %s", (perffil,))
        result_n = self.cursor_uno.fetchone()

        self.cursor_uno.execute("SELECT apellido FROM usuario WHERE id_usuario = %s", (perffil,))
        result_a = self.cursor_uno.fetchone()

        for row in result_n:
            self.nombre_usuario = f"{row}"

        for row_2 in result_a:
            self.apellido_usuario = f"{row_2}"

        self.nombre_completo = f"{self.nombre_usuario} {self.apellido_usuario}"

        return self.nombre_completo

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
    
    def cambiar_contraseña(self):
        try:
    
            id=int(input('¿Cual es tu id?:'))  

            columna='contraseña'
            nuevo_valor=input(f'nueva({columna}):')

            comando_sql= sql.SQL("""
                                 UPDATE {}
                                 SET contraseña=%s
                                 WHERE id_usuario=%s
                                 """).format(sql.Identifier('usuario'))

            self.cursor_uno.execute(comando_sql,(nuevo_valor,id))
            self.conexion1.commit()
            print('Correcto')

        except Exception as a:
            print(f'Error al cambiar contraseña, desde Conexion: {a}')

    def limpiar_terminal(self):
        if os.name == 'nt':
            _ = os.system('cls')

        else:
            _ = os.system('clear')
    

class main:
    def __init__(self):
        con = Conexion()
        #con.Validacion_Perfil(1)

if __name__ == "__main__":
    main()