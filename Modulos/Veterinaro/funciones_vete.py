import psycopg2
from psycopg2 import sql
import os

class FuncinesVete:
    def __init__(self):
        self.conexion = psycopg2.connect("postgresql://neondb_owner:npg_M1nvy9aksESm@ep-raspy-star-afucb7a1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
        self.cursor = self.conexion.cursor()

    def buscarId_unico(self,columna:tuple,id,table:str):
        try:
            columas_safe = [sql.Identifier(c) for c in columna]
            pk_table='id_'+table

            code=sql.SQL('SELECT {} FROM {} WHERE {}=%s').format(
                sql.SQL(', ').join(columas_safe),
                sql.Identifier(table),
                sql.Identifier(pk_table)
            )
            self.cursor.execute(code,(id,))
            datos=self.cursor.fetchone()

            return datos
        
        except Exception as a:
            print(f'Error en funciones de veterinario:{a}')
        
    def insertar_sindevolverId(self,table:str,datos:tuple,columna:tuple):
        try:
            columas_safe = [sql.Identifier(c) for c in columna]
            lugares = [sql.SQL('%s')] * len(datos)

            comando = sql.SQL('INSERT INTO {}({}) VALUES ({})').format(
                sql.Identifier(table),
                sql.SQL(', ').join(columas_safe), 
                sql.SQL(', ').join(lugares)
            )
            
            self.cursor.execute(comando, datos)
            self.conexion.commit() 
            
        except Exception as a:
            print(f'Error en funciones de veterinario:{a}')
            self.conexion.rollback()