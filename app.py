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

@app.route('/where-patient', methods=['GET'])
def mejor_hospital():
    # Get 'dni' from query parameters
    dni = request.args.get('dni', default=None, type=str)
    if dni is None:
        return jsonify({"error": "No DNI provided"}), 400
    
    hosp_inter = controller.get_hospital_by_dni(dni)
    
    if hosp_inter is None:
        return jsonify({"error": "Hospital not found"}), 404
    
    return jsonify(
        {	"id": hosp_inter.id,
			"cant_oxigeno": 2,
            "pacienteData": {
            "id": hosp_inter.id,
            "nombre": hosp_inter.nombres,
            "apellidos": hosp_inter.apellidos,
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

if __name__ == '__main__':
    app.run(debug=True)



#Ubicar hospital de paciente internado
dni = "10893802"
hosp_inter = controller.get_hospital_by_dni(dni)

print("Hospital Internado:  ", hosp_inter.nombre,"\n\n")



#Definiendo los hospitales dentro del distrito del paciente internado
hospitales_distrito = controller.get_hospitales_by_district(hosp_inter.distrito)

#Agregando los hospitales al grafo:
for hospital in hospitales_distrito:
    grafo.add_node(hospital)

#Creando las aristas del grafo. Todos los nodos se unen entre si
grafo.crear_arista()

#Validando los indices de los nodos:
#print(len(grafo.indices))

#Validar la lista de adyacencia del grafo
"""for nodo, aristas in grafo.adyacencia.items():
    
    print(f"Nodo:  {nodo.nombre}\n\nAristas:  ")
    for element in aristas:
        print(f"({element[0].nombre}, {element[1]})")
    print("\n\n")"""

#Obteniendo el precio optimo de balon de oxigeno

hospital_mejor_precio = grafo.breadth_first_search(hosp_inter.nombre,set())
#print("Hospital Optimo:  ", resultado.nombre, " -   Precio Oxigeno:  ", resultado.cost_oxi)
#print("Cantidad Recorrida: ", resultado)
print(f"Busqueda inicial:  {hospital_mejor_precio.nombre}   Precio: {hospital_mejor_precio.cost_oxi}")
print(hospital_mejor_precio.lat)
print(hospital_mejor_precio.lon)

print("---------------------------------------")


#Probando el Quick Union
print("\n\nRealizando busqueda amplificada")

grafo.ampliar_grafo(hosp_inter.nombre)
print("Total Nodos:  ",len(grafo.nodos))
print("Distritos Recorridos:  ",grafo.distritos_recorridos)

resultado = grafo.breadth_first_search(hosp_inter.nombre,set())
#print("Hospital Optimo:  ", resultado.nombre, " -   Precio Oxigeno:  ", resultado.cost_oxi)
print(f"Nueva Busqueda:  {resultado.nombre}   Precio: {resultado.cost_oxi}")


"""grafo.ampliar_grafo(hosp_inter.nombre)
print("Total Nodos:  ",len(grafo.nodos))
print("Distritos Recorridos:  ",grafo.distritos_recorridos)

grafo.ampliar_grafo(hosp_inter.nombre)
print("Total Nodos:  ",len(grafo.nodos))
print("Distritos Recorridos:  ",grafo.distritos_recorridos)

grafo.ampliar_grafo(hosp_inter.nombre)
print("Total Nodos:  ",len(grafo.nodos))
print("Distritos Recorridos:  ",grafo.distritos_recorridos)"""

"""for nodo, aristas in grafo.adyacencia.items():
    
    print(f"Nodo:  {nodo.nombre}\n\nAristas:  ")
    for element in aristas:
        print(f"({element[0].nombre}, {element[1]})")
    print("\n\n")
"""


#h = grafo.nodos[27]
#El objeto hosp_inter no es el mismo al que se encuentra en el nodo, pese a tener los mismos atributos
#print(h.nombre == hosp_inter.nombre)





"""hospitales = controller.get_hospitales()

for hospital in hospitales:
    grafo.add_node(hospital)
    #print(f"id: {hospital.id} nombre: {hospital.nombre}" )

grafo.crear_arista()


for nodo, aristas in grafo.adyacencia.items():
    
    print(f"Nodo:  {nodo.nombre}  Aristas:  ",end=" ")
    for element in aristas:
        print(f"({element[0].nombre}, {element[1]})")

cant_hospitales = grafo.breadth_first_search(grafo.nodos[0],set())
print(cant_hospitales)
#hospitales_optimos = controller.get_hospitales_by_price(costo_optimo)


#for element in hospitales_optimos:
    #print(f"id:  {element.id}  Nombre:  {element.nombre}  Precio: {element.cost_oxi}")"""


