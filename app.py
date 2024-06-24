from grafo import GrafoHospitales
from hospitalcontroller import HospitalController




#Definiendo diccionario de adyacencia de distritos:

adyacencia_distritos={"San Juan de Lurigancho": ["Cercado de Lima"],
                      "Cercado de Lima":["La Victoria","Breña","Pueblo Libre","Jesus Maria","San Juan de Lurigancho"],
                      "La Victoria":["Cercado de Lima","Lince","San Borja","Jesus Maria","Breña"],
                      "San Luis":["San Borja","La Victoria"],
                      "Surquillo": ["San Isidro","San Borja","Miraflores"],
                      "San Borja":["La Victoria","San Luis","Lince","San Isidro","Surquillo"],
                      "Breña":["Cercado de Lima","La Victoria","Jesus Maria","Pueblo Libre"],
                      "Lince":["La Victoria","San Borja","San Isidro","Magdalena del Mar","Jesus Maria"],
                      "Magdalena del Mar":["San Isidro","Jesus Maria","Pueblo Libre","San Miguel"],
                      "San Isidro":["Magdalena del Mar","Jesus Maria","Lince","La Victoria","San Borja","Surquillo","Miraflores"],
                      "San Miguel": ["Jesus Maria","Magdalena del Mar"],
                      "Miraflores":["Surquillo","San Isidro"],
                      "Jesus Maria":["Pueblo Libre","Magdalena del Mar","Lince","La Victoria","San Isidro","Breña","Cercado de Lima"],
                      "Pueblo Libre":["San Miguel","Magdalena del Mar","Jesus Maria","Breña","Cercado de Lima"]
                      }



#Controlador de Hospitales
controller = HospitalController()
#Creando el Grafo
grafo = GrafoHospitales()

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/internados', methods=['GET'])
def mejor_hospital():
    dni = request.args.get('dni', default=None, type=str)
    if dni is None:
        return jsonify({"error": "No DNI provided"}), 400
    
    hosp_inter = controller.get_hospital_by_dni(dni)
    
    if hosp_inter is None:
        return jsonify({"error": "Hospital not found"}), 404
    
    internado = controller.get_paciente_data(dni)
    
    datos_internamiento = controller.get_paciente_internado_data(dni)
    
    return jsonify(
        {    "id": hosp_inter.id,
            "cant_oxigeno": datos_internamiento.cant_oxi,
            "pacienteData": {
            "id": internado.id,
            "nombre": internado.nombres,
            "apellidos": internado.apellidos,
            "diagnostico": internado.diagnostico
            },
            "hospitalData" : {
                "id_hospital": hosp_inter.id,
                "nombre": hosp_inter.nombre, 
                "direccion": hosp_inter.direccion,
                "distrito": hosp_inter.distrito,
                "oxigeno_disponible": hosp_inter.oxi_disp,
                "costo_oxi": hosp_inter.cost_oxi,
                "latitud": hosp_inter.lat, 
                "longitud": hosp_inter.lon
         }
        }
        )


@app.route('/obtener-proveedor', methods=['GET'])
def obtener_proveedor():
    dni = request.args.get('dni', default=None, type=str)
    if dni is None:
        return jsonify({"error": "No DNI provided"}), 400
    
    hosp_inter = controller.get_hospital_by_dni(dni)
    
    if hosp_inter is None:
        return jsonify({"error": "Hospital not found"}), 404
    
    hosp_inter = controller.get_hospital_by_dni(dni)
    hospitales_distrito = controller.get_hospitales_by_district(hosp_inter.distrito)
    for hospital in hospitales_distrito:
        grafo.add_node(hospital)
    grafo.crear_arista()
    hospital_mejor_precio = grafo.breadth_first_search(hosp_inter.nombre,set())
    return jsonify(
        {
            "nombre": hospital_mejor_precio.nombre,
            "costo_oxigeno": hospital_mejor_precio.cost_oxi,
            "latitud": hospital_mejor_precio.lat,
            "longitud": hospital_mejor_precio.lon
         }
    )

@app.route('/obtener-proveedor-ampliado', methods=['GET'])
def obtener_proveedor_ampliado():
    dni = request.args.get('dni', default=None, type=str)
    if dni is None:
        return jsonify({"error": "No DNI provided"}), 400
    
    hosp_inter = controller.get_hospital_by_dni(dni)
    
    if hosp_inter is None:
        return jsonify({"error": "Hospital not found"}), 404
    
    hosp_inter = controller.get_hospital_by_dni(dni)
    hospitales_distrito = controller.get_hospitales_by_district(hosp_inter.distrito)
    for hospital in hospitales_distrito:
        grafo.add_node(hospital)
    grafo.crear_arista()
    grafo.ampliar_grafo(hosp_inter.nombre)
    resultado = grafo.breadth_first_search(hosp_inter.nombre,set())
    return jsonify(
        {
            "nombre": resultado.nombre,
            "costo_oxigeno": resultado.cost_oxi,
            "latitud": resultado.lat,
            "longitud": resultado.lon
         }
    )


if __name__ == '__main__':
    app.run(port=8080)
