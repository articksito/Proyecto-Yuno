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
            for dato in columnas:
                partes = dato.split('.')
                if len(partes) == 2:
                    nombre_tabla, nombre_columna = partes
                    columna_safe.append(
                        sql.SQL('{}.{}').format(
                            sql.Identifier(nombre_tabla),
                            sql.Identifier(nombre_columna)
                        )
                    )
                else:
                    columna_safe.append(sql.Identifier(dato))
            
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
    def insertar_datos(self, table: str, datos: tuple = None, columna: tuple = None):
        try:
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
            
        except psycopg2.Error as error:
            print(f"Error en db conexion al insertar: {error}")
            self.conexion.rollback()
            return None