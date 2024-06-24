import mysql.connector
from mysql.connector import Error

def Conexion():
    try:
        connection = mysql.connector.connect(host="localhost",user = "root", password = "admin", port="3306",database="prueba")
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
    
class Paciente:
    def __init__(self, id = None, nombres = None, apellidos = None, diagnostico = None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.diagnostico = diagnostico
    
    def insertar_paciente(self):
        connection = Conexion()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "Insert into pacientes(nombres,apellidos,diagnostico) values(%s,%s,%s)"
                values= (self.nombres,self.apellidos,self.diagnostico)
                cursor.execute(query,values)
                connection.commit()
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    connection.close()
    
    def obtener_paciente(self, dni):
        connection = Conexion()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "select * from pacientes where dni = %s"
                values = (dni)
                cursor.execute(query, values)
                resultado = cursor.fetchall()
                return Paciente(resultado[0], resultado[1], resultado[2], resultado[3])
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    connection.close()