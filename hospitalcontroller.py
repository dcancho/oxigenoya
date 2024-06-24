import mysql.connector
from mysql.connector import Error
from hospital import Hospital
from internado import Internado
from paciente import Paciente


def Conexion():
    try:
        connection = mysql.connector.connect(host="oxigenoya-db.mysql.database.azure.com",user = "oxigenoya", password = "Admin123admin", port="3306",database="prueba")
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

class HospitalController:
    
    def __init__(self):
        
        try:
            connection = mysql.connector.connect(host="oxigenoya-db.mysql.database.azure.com",user = "oxigenoya", password = "Admin123admin", port="3306",database="prueba")
            if connection.is_connected():
                print("Conexion Exitosa")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")




    def get_hospitales(self):

        hospitales = []
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "select * from hospitales"
                cursor.execute(query)
                resultado = cursor.fetchall()
                for id,nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon in resultado:
                    hospital = Hospital(id,nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon)
                    hospitales.append(hospital)
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if self.connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    self.connection.close()
        
        return hospitales


    def get_hospital_by_dni(self, dni):
        
        self.connection =Conexion()
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "select h.id,h.nombre,h.direccion,h.distrito,h.oxigeno_disponible,h.costo_oxigeno,h.latitud,h.longitud from hospitales h inner join internados i on h.id = i.id_hospital where i.dni = %s"
                cursor.execute(query,(dni,))
                resultado = cursor.fetchone()
                
                #for id,nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon in resultado:
                    #hospital = Hospital(id,nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon)
                id = resultado[0]
                nombre = resultado[1]
                direccion = resultado[2]
                distrito = resultado[3]
                oxi_disp = resultado[4]
                costo_oxi = resultado[5]
                lat = resultado[6]
                lon = resultado[7]
                hospital = Hospital(id,nombre,direccion,distrito,oxi_disp,costo_oxi,lat,lon)

            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            else:
                if self.connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    self.connection.close()
        return hospital
    

    def get_hospitales_by_district(self,distrito):
        hospitales = []
        self.connection =Conexion()
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "select * from hospitales where distrito = %s"
                cursor.execute(query,(distrito,))
                resultado = cursor.fetchall()
                for id,nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon in resultado:
                    hospital = Hospital(id,nombre,direccion,distrito,oxi_disp,cost_oxi,lat,lon)
                    hospitales.append(hospital)
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            else:
                if self.connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    self.connection.close()
        return hospitales


    def get_hospitales_by_price(self,cost_oxi):
        hospitales = []
        self.connection =Conexion()
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "select * from hospitales where costo_oxigeno=%s"
                cursor.execute(query,(cost_oxi,))
                resultado = cursor.fetchall()
                for id,nombre,direccion,oxi_disp,cost_oxi,lat,lon in resultado:
                    hospital = Hospital(id,nombre,direccion,oxi_disp,cost_oxi,lat,lon)
                    hospitales.append(hospital)
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            else:
                if self.connection.is_connected():
                    cursor.close()  # Cerrar el cursor
                    self.connection.close()
        return hospitales
    
    def get_paciente_data(self, dni):
        self.connection =Conexion()
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "select * from pacientes where dni = %s"
                cursor.execute(query,(dni,))
                resultado = cursor.fetchone()
                id = resultado[0]
                nombre = resultado[1]
                apellido = resultado[2]
                diagnostico = resultado[3]
                return Paciente(id,nombre,apellido,diagnostico)
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if self.connection.is_connected():
                    cursor.close()
    
    def get_paciente_internado_data(self, dni):
        self.connection =Conexion()
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "select * from internados where dni = %s"
                cursor.execute(query,(dni,))
                resultado = cursor.fetchone()
                id = resultado[0]
                id_hospital = resultado[1]
                cant_oxi = resultado[2]
                return Internado(id,id_hospital,cant_oxi)
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if self.connection.is_connected():
                    cursor.close()

    def hacer_pedido(self, id_hospital, cant_oxi):
        self.connection = Conexion()
        if self.connection is not None:
            try:
                cursor = self.connection.cursor()
                query = "update hospitales set oxigeno_disponible = oxigeno_disponible - %s where id = %s"
                values = (cant_oxi, id_hospital)
                cursor.execute(query, values)
                self.connection.commit()
            except Error as e:
                print(f"Error al insertar en MySQL: {e}")
            finally:
                if self.connection.is_connected():
                    cursor.close()
                    


"""controlador = HospitalController()

hospital = controlador.get_hospital_by_dni("10069175")

hospitales_distrito = controlador.get_hospitales_by_district(hospital.distrito)

for h in hospitales_distrito:
    print(h.nombre, "-  ", h.direccion, "-  ", h.id)    

#print(hospital.nombre, "-  ", hospital.direccion, "-  ", hospital.id)"""