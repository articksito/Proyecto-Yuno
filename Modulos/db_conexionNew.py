import psycopg2
from psycopg2 import sql
import os

class Conexion:
    def __init__(self):
        # Cadena de conexión existente
        self.conexion = psycopg2.connect("postgresql://neondb_owner:npg_M1nvy9aksESm@ep-raspy-star-afucb7a1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
        self.cursor = self.conexion.cursor()
    
    #Consulta total
    def consultar_tabla(self,columnas:tuple,tabla:str,joins:list=None ,filtro:str=None,campo_filtro:str=None,orden:tuple=None):
        try:
            columna_safe = []
            for dato in columnas: #Verifica
                partes = dato.split('.')#Las separa
                if len(partes) == 2: 
                    nombre_tabla, nombre_columna = partes 
                    columna_safe.append(
                        sql.SQL('{}.{}').format(
                            sql.Identifier(nombre_tabla),
                            sql.Identifier(nombre_columna) 
                        )
                    )
                else:
                    columna_safe.append(sql.Identifier(dato))#Lo salta
            
            comando=[]
            comando.append(sql.SQL('SELECT {}').format(sql.SQL(', ').join(columna_safe)))
            comando.append(sql.SQL('FROM {}').format(sql.Identifier(tabla)))
            
            if joins:
                for tabla_unir, tabla_base in joins:
                    comando.append(
                        sql.SQL('JOIN {} ON {}.{} = {}.{}').format(
                            sql.Identifier(tabla_unir),            
                            sql.Identifier(tabla_base),            
                            sql.Identifier('fk_' + tabla_unir),    
                            sql.Identifier(tabla_unir),            
                            sql.Identifier('id_' + tabla_unir)     
                        )
                    )

            params = None
            if filtro and campo_filtro:
                if '.' in campo_filtro: #Si la condicion viene como mascota.etc
                    t_filtro, c_filtro = campo_filtro.split('.')
                    col_identifier = sql.SQL('{}.{}').format(sql.Identifier(t_filtro), sql.Identifier(c_filtro))
                else:
                    col_identifier = sql.Identifier(campo_filtro)

                comando.append(sql.SQL('WHERE {} ILIKE %s').format(col_identifier)) 
                
                params = (f"%{filtro}%",)
            
            if orden:
                orden_safe = []
                for dato in orden:

                    if '.' in dato:
                        t_orden, c_orden = dato.split('.')
                        orden_safe.append(sql.SQL('{}.{} ASC').format(sql.Identifier(t_orden), sql.Identifier(c_orden)))
                    else:
                        orden_safe.append(sql.SQL('{} ASC').format(sql.Identifier(dato)))
                
                comando.append(sql.SQL('ORDER BY {}').format(sql.SQL(', ').join(orden_safe)))

            comando_final = sql.SQL(' ').join(comando) #Funciona sin el where, por eso los if de abajo

            if params:
                self.cursor.execute(comando_final, params)
            else:
                self.cursor.execute(comando_final)
      
            devolver = self.cursor.fetchall()

            print('Consulta correcta en db conexion')
            return devolver

        except Exception as a:
            print(f'Error en db conexion al consultar: {a}')
            return None
        
        #Consultar uno
    def consultar_registro(self, tabla: str, id_columna: str, id_valor, columnas=None, joins: str = ""):

        try:
            if columnas:
                cols_sql = sql.SQL(", ").join([
                    sql.SQL(c) if "." in c else sql.Identifier(c)
                    for c in columnas
                ])
            else:
                cols_sql = sql.SQL("*")

            # --- WHERE ---
            # Manejo seguro de tabla.id vs id simple
            if "." in id_columna:
                tabla_id, col_id = id_columna.split(".")
                where_sql = sql.SQL("{}.{}").format(sql.Identifier(tabla_id), sql.Identifier(col_id))
            else:
                where_sql = sql.Identifier(id_columna)

            joins_sql = sql.SQL(joins) if joins else sql.SQL("")

            query = sql.SQL("SELECT {cols} FROM {tabla} {joins} WHERE {where} = %s").format(
                cols=cols_sql,
                tabla=sql.Identifier(tabla),
                joins=joins_sql,
                where=where_sql
            )

            self.cursor.execute(query, (id_valor,))

            print('Consulta correcta en db conexion')
            return self.cursor.fetchone()

        except Exception as e:
            print(f"Error en db conexion al consultar: {e}")
            return None

        
    #Insertar
    def insertar_datos(self, table: str, datos: tuple = None, columna: tuple = None,retornar:bool=True):
        try:
            if retornar: #Si ocupa retornar que es lo usual.
                columas_safe = [sql.Identifier(c) for c in columna]
                lugares = [sql.SQL('%s')] * len(datos)

                pk_columna = 'id_' + table

                comando = sql.SQL('INSERT INTO {}({}) VALUES ({}) RETURNING {}').format(
                    sql.Identifier(table),
                    sql.SQL(', ').join(columas_safe), 
                    sql.SQL(', ').join(lugares),
                    sql.Identifier(pk_columna)
                )
                
                self.cursor.execute(comando, datos)
                row = self.cursor.fetchone()
                id_generado = row[0] if row else None
                
                self.conexion.commit() 
                print("Insert correcto en db conexion")
                return id_generado
            else: #Para los que no la acupan, como tablas intermedias.
                columas_safe = [sql.Identifier(c) for c in columna]
                lugares = [sql.SQL('%s')] * len(datos)

                comando = sql.SQL('INSERT INTO {}({}) VALUES ({})').format(
                    sql.Identifier(table),
                    sql.SQL(', ').join(columas_safe), 
                    sql.SQL(', ').join(lugares)
                )
                
                self.cursor.execute(comando, datos)
                self.conexion.commit()

                print("Insert correcto en db conexion") 

        except psycopg2.Error as error:
            print(f"Error en db conexion al insertar: {error}")
            self.conexion.rollback()
            return None

    #Modificar  
    def editar_registro(self, id: int, datos: dict, tabla: str, id_columna: str):
        try:
            comando = []
            valores = []

            for columna, valor in datos.items():
                comando.append(sql.SQL("{} = %s").format(sql.Identifier(columna)))
                valores.append(valor)

            unir = sql.SQL(', ').join(comando)

            comando_sql = sql.SQL("""
                                 UPDATE {}
                                 SET {}
                                 WHERE {} = %s
                                 """).format(sql.Identifier(tabla), unir, sql.Identifier(id_columna))
            
            valores.append(id)

            self.cursor.execute(comando_sql, tuple(valores))
            self.conexion.commit()
            print('Editar Correcto en db conexion')
            return True
        except Exception as a:
            print(f"Error al editar registro/s en db conexion: {a}")
            self.conexion.rollback()
            return False
    
     # ----------------------------
    # MÉTODOS DE USUARIO / LOGIN
    # ----------------------------
    def Validacion_usuario(self, id_user: int):
        self.id_user = id_user
        
        try:
            sql_q = "SELECT 1 FROM usuario WHERE id_usuario = %s"
            self.cursor.execute(sql_q, (id_user,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception:
            return False

    def Validacion_Perfil(self, perffil: int):
        try:
            self.cursor.execute("SELECT rol FROM usuario WHERE id_usuario = %s", (perffil,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            return ""
        except Exception:
            return ""

    def Nombre_Usuario(self, perffil: int):
        try:
            self.cursor.execute("SELECT nombre, apellido FROM usuario WHERE id_usuario = %s", (perffil,))
            result = self.cursor.fetchone()
            if result:
                return f"{result[0]} {result[1]}"
            return ""
        except Exception:
            return ""

    def Validacion_contrasena(self, user_pwd):
        try:
            # Asumiendo que self.id_user fue seteado previamente
            if not hasattr(self, 'id_user'): return False
            
            sql_q = "SELECT contraseña FROM usuario WHERE id_usuario = %s"
            self.cursor.execute(sql_q, (self.id_user,))
            row = self.cursor.fetchone()
            
            if row and row[0] == user_pwd:
                return True
            return False
        except Exception:
            return False
    
    def cambiar_contraseña(self):
        try:
            id_u = int(input('¿Cual es tu id?:'))  
            nuevo_valor = input(f'nueva contraseña:')

            comando_sql = sql.SQL("""
                                 UPDATE {}
                                 SET contraseña = %s
                                 WHERE id_usuario = %s
                                 """).format(sql.Identifier('usuario'))

            self.cursor.execute(comando_sql, (nuevo_valor, id_u))
            self.conexion.commit()
            print('Correcto')
        except Exception as a:
            print(f'Error al cambiar contraseña: {a}')
            self.conexion.rollback()
