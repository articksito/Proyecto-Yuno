import psycopg2
from psycopg2 import sql
import os

class Conexion:
    def __init__(self):
        # Cadena de conexión existente
        self.conexion = psycopg2.connect("postgresql://neondb_owner:npg_M1nvy9aksESm@ep-raspy-star-afucb7a1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
        self.cursor = self.conexion.cursor()
    
    #Consulta
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
                    # Asumimos orden Ascendente por defecto
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
            return devolver

        except Exception as a:
            print(f'Error en db conexion al consultar: {a}')