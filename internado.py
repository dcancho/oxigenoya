import mysql.connector
from mysql.connector import Error

def Conexion():
    try:
        connection = mysql.connector.connect(host="oxigenoya-db.mysql.database.azure.com",user = "oxigenoya", password = "Admin123admin", port="3306",database="prueba")
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

class Internado:
    def __init__(self,dni,id_hospital,cant_oxi):
        self.dni = dni
        self.id_hospital = id_hospital
        self.cant_oxi = cant_oxi


    def insertar_internado(self):
        connection = Conexion()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "Insert into internados(dni,id_hospital,cant_oxigeno) values(%s,%s,%s)"
                values= (self.dni,self.id_hospital,self.cant_oxi)
                cursor.execute(query,values)
                connection.commit()
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    connection.close()
            
    def obtener_internado(self, dni):
        connection = Conexion()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "select * from internados where dni = %s"
                values = (dni)
                cursor.execute(query, values)
                resultado = cursor.fetchall()
                return Internado(resultado[0], resultado[1], resultado[2])
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()
    