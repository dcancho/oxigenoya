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

class Hospital:
    def __init__(self,id = None,nombre=None,direccion=None,distrito = None,oxi_disp=None,cost_oxi=None,lat=None,lon=None):
        self.id= id
        self.nombre = nombre
        self.direccion = direccion
        self.distrito = distrito
        self.oxi_disp = oxi_disp
        self.cost_oxi = cost_oxi
        self.lat = lat
        self.lon = lon

    def insertar_hospital(self):
        connection = Conexion()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "Insert into hospitales(nombre,direccion,distrito,oxigeno_disponible,costo_oxigeno,latitud,longitud) values(%s,%s,%s,%s,%s,%s,%s)"
                values= (self.nombre,self.direccion,self.distrito,self.oxi_disp,self.cost_oxi,self.lat,self.lon)
                cursor.execute(query,values)
                connection.commit()
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    connection.close()
    
    def obtener_hospitales(self):
        connection = Conexion()
        if connection is not None:
            try:
                cursor = connection.cursor()
                query = "select * from hospitales where id >=1 and id <=8"
                cursor.execute(query)
                resultado = cursor.fetchall()
                for id,nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon in resultado:
                    print("Nombre: ",nombre)
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    connection.close()