import psycopg2
from psycopg2 import sql
import os

class Conexion:
    def __init__(self):
        # Cadena de conexión existente
        self.conexion1 = psycopg2.connect("postgresql://neondb_owner:npg_M1nvy9aksESm@ep-raspy-star-afucb7a1-pooler.c-2.us-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
        self.cursor_uno = self.conexion1.cursor()

    # ----------------------------
    # UTILIDADES
    # ----------------------------
    def truncase(self, table: str):
        try:
            code = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY CASCADE").format(sql.Identifier(table))
            self.cursor_uno.execute(code)
            self.conexion1.commit()
            print(f'{table} reiniciada')
        except Exception as a:
            print(f'Error en conexion: {a}')
            if hasattr(self, 'conexion1'):
                self.conexion1.rollback()

    def cerrar_conexion(self):
        if hasattr(self, 'cursor_uno') and self.cursor_uno:
            self.cursor_uno.close()
        if hasattr(self, 'conexion1') and self.conexion1:
            self.conexion1.close()
        print('Cerrado, vuelva pronto')

    def limpiar_terminal(self):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    # ----------------------------
    # CONSULTAS (SELECTS)
    # ----------------------------
    def Select_users(self, table: str):
        try:
            code = sql.SQL("SELECT * FROM {} ").format(sql.Identifier(table))
            self.cursor_uno.execute(code)
            table = self.cursor_uno.fetchall()
            return table
        except Exception as a:
            print(f"Error en Select_users: {a}")
            return []

    def select_con_filtro(self, table: str, condition_column: str, condition_value):
        try: 
            buscador = sql.SQL("SELECT * FROM {} WHERE {} ILIKE %s").format(
                sql.Identifier(table),
                sql.Identifier(condition_column)
            )
            if condition_column.startswith('id_'):
                # Si es ID, buscamos exacto (convertido a str para el ILIKE o cambiar logica)
                # Nota: ILIKE espera texto, si id es int en BD, postgres suele castaerlo, 
                # pero lo ideal sería '=' para IDs. Mantengo tu lógica original.
                search_value = str(condition_value)
            else:
                search_value = f"%{condition_value}%"
            
            self.cursor_uno.execute(buscador, (search_value,))
            resultados = self.cursor_uno.fetchall()
            return resultados 
        except Exception as a:
            print(f'Error al seleccionar la busqueda: {a}')
            return []

    def select_citas_por_cliente(self, id_cliente):
        try:
            especial = """SELECT c.* FROM cita c JOIN mascota m ON c.fk_mascota = m.id_mascota WHERE m.fk_cliente = %s; """
            self.cursor_uno.execute(especial , (id_cliente,))
            return self.cursor_uno.fetchall()
        except Exception as e:
            print(f'Error al buscar citas por cliente: {e}')
            return []

    def selcionar_dato(self, dato, table: str, columna: str):
        try:
            comando_sql = sql.SQL("SELECT {} FROM {} WHERE {} = %s").format(
                sql.Identifier(columna),
                sql.Identifier(table),
                sql.Identifier(columna)
            )
            self.cursor_uno.execute(comando_sql, (dato,))
            a = self.cursor_uno.fetchone()
            return a[0] if a else None
        except Exception as a:
            print(f'Error al seleccionar dato: {a}')
            return None

    # --- FUNCIÓN PRINCIPAL DE CONSULTA (Soporta JOINs y Columnas específicas) ---
    def consultar_registro(self, tabla: str, id_columna: str, id_valor, columnas=None, joins: str = ""):
        """
        Busca un registro por ID y retorna las columnas solicitadas.
        Permite agregar JOINS manuales como texto SQL.
        Retorna una tupla con los valores o None.
        """
        try:
            # --- SELECT columns ---
            if columnas:
                # Si la columna tiene un punto (ej: tabla.columna), se usa sql.SQL directo
                # Si no, se usa Identifier para seguridad
                cols_sql = sql.SQL(", ").join([
                    sql.SQL(c) if "." in c else sql.Identifier(c)
                    for c in columnas
                ])
            else:
                cols_sql = sql.SQL("*")

            # --- WHERE ---
            # Manejo seguro de tabla.id vs id simple
            if "." in id_columna:
                # Si viene como "cita.id_cita"
                tabla_id, col_id = id_columna.split(".")
                where_sql = sql.SQL("{}.{}").format(sql.Identifier(tabla_id), sql.Identifier(col_id))
            else:
                where_sql = sql.Identifier(id_columna)

            # --- JOINS ---
            joins_sql = sql.SQL(joins) if joins else sql.SQL("")

            # --- Construcción final ---
            query = sql.SQL("SELECT {cols} FROM {tabla} {joins} WHERE {where} = %s").format(
                cols=cols_sql,
                tabla=sql.Identifier(tabla),
                joins=joins_sql,
                where=where_sql
            )

            self.cursor_uno.execute(query, (id_valor,))
            return self.cursor_uno.fetchone()

        except Exception as e:
            print(f"Error en consultar_registro: {e}")
            # No lanzamos raise para evitar crash en la UI, retornamos None
            return None

    # ----------------------------
    # INSERCIONES
    # ----------------------------
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
            
            self.cursor_uno.execute(comando, datos)
            row = self.cursor_uno.fetchone()
            id_generado = row[0] if row else None
            
            self.conexion1.commit() 
            print("Insert correcto")
            return id_generado
            
        except psycopg2.Error as error:
            print(f"Error en insertar_datos: {error}")
            self.conexion1.rollback()
            return None

    # ----------------------------
    # ACTUALIZACIONES (UPDATE)
    # ----------------------------
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

            self.cursor_uno.execute(comando_sql, tuple(valores))
            self.conexion1.commit()
            print('Editar Correcto')
            return True
        except Exception as a:
            print(f"Error al editar registro/s: {a}")
            self.conexion1.rollback()
            return False

    def update_registro(self, id, datos: dict, tabla: str, id_columna: str):
        """
        Versión alternativa de editar_registro, usada en algunas pantallas.
        """
        if not datos:
            print("No se proporcionaron datos para actualizar.")
            return False

        try:
            columnas = [sql.Identifier(col) for col in datos.keys()]
            asignaciones = [
                sql.SQL("{} = %s").format(col)
                for col in columnas
            ]

            query = sql.SQL("""
                UPDATE {tabla}
                SET {asignaciones}
                WHERE {id_columna} = %s
            """).format(
                tabla=sql.Identifier(tabla),
                asignaciones=sql.SQL(", ").join(asignaciones),
                id_columna=sql.Identifier(id_columna)
            )

            valores = list(datos.values()) + [id]

            self.cursor_uno.execute(query, valores)
            self.conexion1.commit()
            print("Registro actualizado correctamente.")
            return True

        except Exception as e:
            self.conexion1.rollback()
            print(f"Error al update_registro: {e}")
            return False

    # ----------------------------
    # ELIMINAR (DELETE)
    # ----------------------------
    def eliminar_registro(self, id: int, tabla: str, id_columna: str):
        try:
            comando_sql = sql.SQL("""
                        DELETE FROM {}
                        WHERE {} = %s
                                """).format(sql.Identifier(tabla), sql.Identifier(id_columna))
            self.cursor_uno.execute(comando_sql, (id,))
            self.conexion1.commit()
            print('Eliminado correctamente.')
            return True
        except Exception as a:
            print(f"Error al eliminar registro: {a}")
            self.conexion1.rollback()
            return False

    # ----------------------------
    # MÉTODOS DE USUARIO / LOGIN
    # ----------------------------
    def Validacion_usuario(self, id_user: int):
        self.id_user = id_user
        
        try:
            sql_q = "SELECT 1 FROM usuario WHERE id_usuario = %s"
            self.cursor_uno.execute(sql_q, (id_user,))
            result = self.cursor_uno.fetchone()
            return result is not None
        except Exception:
            return False

    def Validacion_Perfil(self, perffil: int):
        try:
            self.cursor_uno.execute("SELECT rol FROM usuario WHERE id_usuario = %s", (perffil,))
            result = self.cursor_uno.fetchone()
            if result:
                return result[0]
            return ""
        except Exception:
            return ""

    def Nombre_Usuario(self, perffil: int):
        try:
            self.cursor_uno.execute("SELECT nombre, apellido FROM usuario WHERE id_usuario = %s", (perffil,))
            result = self.cursor_uno.fetchone()
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
            self.cursor_uno.execute(sql_q, (self.id_user,))
            row = self.cursor_uno.fetchone()
            
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

            self.cursor_uno.execute(comando_sql, (nuevo_valor, id_u))
            self.conexion1.commit()
            print('Correcto')
        except Exception as a:
            print(f'Error al cambiar contraseña: {a}')
            self.conexion1.rollback()

    # ==============================================
    #   FUNCIONES ESPECÍFICAS PARA PANTALLAS UI
    # ==============================================

    def obtener_stats_citas(self):
        """
        Usado en Dashboard Admin. Cuenta citas por estado.
        """
        try:
            query = "SELECT estado, COUNT(*) FROM cita GROUP BY estado"
            self.cursor_uno.execute(query)
            resultados = self.cursor_uno.fetchall()
            
            stats = {row[0]: row[1] for row in resultados}
            
            defaults = ["Confirmada", "Completada", "Cancelada", "Pendiente"]
            for d in defaults:
                if d not in stats:
                    stats[d] = 0
            return stats
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {"Confirmada": 0, "Completada": 0, "Cancelada": 0, "Pendiente": 0}

    def obtener_todos_pacientes(self):
        """
        Usado en UI_Pacientes. Retorna la lista para la tabla.
        Selecciona 5 columnas para evitar error de índice en la UI.
        """
        try:
            # Se agrega 'padecimientos' como la 5ta columna (índice 4)
            # Si no existe en tu tabla, cámbialo por otra columna o null
            query = "SELECT id_mascota, nombre, especie, raza FROM mascota ORDER BY id_mascota ASC"
            
            self.cursor_uno.execute(query)
            resultados = self.cursor_uno.fetchall()
            return resultados
        except Exception as e:
            print(f"Error al obtener pacientes: {e}")
            return []
    


class main:
    def __init__(self):
        con = Conexion()
        # con.Validacion_Perfil(1)

if __name__ == "__main__":
    main()