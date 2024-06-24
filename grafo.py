from collections import deque
from prueba import distancia
from hospitalcontroller import HospitalController
from hospital import Hospital
class GrafoHospitales:

    def __init__(self):
        self.nodos= []
        self.adyacencia={}
        self.labels={}
        self.indices=[]
        #self.hosp_internado=None
        self.adyacencia_distritos={"San Juan de Lurigancho": ["Cercado de Lima"],
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

        self.distritos_recorridos=set()

    def add_node(self,hospital):
        if hospital not in self.nodos:
            self.nodos.append(hospital)
            self.labels[hospital.nombre]=hospital
            self.indices.append(hospital.distrito)
            if hospital.distrito not in self.distritos_recorridos:
                self.distritos_recorridos.add(hospital.distrito)
        elif hospital in self.nodos:
            print(f"El nodo ya se encuentra en el grafo")
      
 

    def add_nodes(self,hospitales):
        for hospital in hospitales:
            self.add_node(hospital)
    
    def create_edge(self,nodo1,nodo2):

        dist = distancia(nodo1,nodo2)
        #nodo1 = self.labels[nodo1]
        #nodo2 = self.labels[nodo2]

        if nodo1 in self.nodos and nodo2 in self.nodos:
            temp = []
            value = (nodo2,dist)
            if nodo1 not in self.adyacencia:
                temp.append(value)
                self.adyacencia[nodo1]=temp
            elif nodo1 in self.adyacencia:
                temp.extend(self.adyacencia[nodo1])
                temp.append(value)
                self.adyacencia[nodo1]=temp


    def crear_arista(self):
        for i in range(len(self.nodos)):
            for j in range(i+1,len(self.nodos)):
                self.create_edge(self.nodos[i],self.nodos[j])
                self.create_edge(self.nodos[j],self.nodos[i])
    
    def breadth_first_search(self, hospital_name,visited):
        hospital =  self.labels[hospital_name]
        hosp_optimo = hospital
        queue = deque([hospital])
        while len(queue) != 0:
            hospital = queue.popleft()
            if hospital not in visited:
                if hospital.cost_oxi < hosp_optimo.cost_oxi:
                    hosp_optimo = hospital
                #print(hospital.nombre)
                visited.add(hospital)
                neighbors = self.adyacencia.get(hospital, [])
                for neighbor in neighbors:
                    if neighbor[0] not in visited:
                        queue.append(neighbor[0])
        return hosp_optimo
    
    def quick_union(self,hospital1,hospital2):
        pos_h1 = self.nodos.index(hospital1)
        pos_h2 = self.nodos.index(hospital2)
        
        self.indices[pos_h2] = hospital1.nombre
        self.create_edge(hospital1,hospital2)
        self.create_edge(hospital2,hospital1)

    #Enviar como parametro el nombre del hospital al cual se debera unir el nuevo grafo
    def ampliar_grafo(self,hospital_name):
        hospital_padre = self.labels[hospital_name]
        controlador = HospitalController()
        grafo_aux = GrafoHospitales()
        set_distritos_aux = list(self.distritos_recorridos)
        if len(set_distritos_aux) == 14:
            print("Busqueda amplificada al maximo. Ya no se puede expandir el area de busqueda")
        else:
            for district in set_distritos_aux: #recorriendo los distritos registrados en el set()
                
                adyacentes = self.adyacencia_distritos.get(district,[])#obteniendo los distritos adyacentes del diccionario de distritos
                for distrito in adyacentes:#recorriendo uno por uno los distritos
                    if distrito not in set_distritos_aux:#verificando si el distrito no fue añadido al set()
                        self.distritos_recorridos.add(distrito)#agregando el nuevo distrito al set
                        hospitales = controlador.get_hospitales_by_district(distrito)
                        grafo_aux.add_nodes(hospitales)
                        grafo_aux.crear_arista()
                        #definiendo el hospital del grafo auxiliar para aplicar el quick union al grafo principal
                        hospital_union = grafo_aux.nodos[0]
                        #Agregando los nodos y aristas del grafo auxiliar al grafo principal
                        self.nodos.extend(grafo_aux.nodos)
                        self.adyacencia.update(grafo_aux.adyacencia)
                        self.labels.update(grafo_aux.labels)
                        self.indices.extend(grafo_aux.indices)
                        self.quick_union(hospital_padre,hospital_union)
                        grafo_aux.nodos = []
                        grafo_aux.adyacencia = {}
                        grafo_aux.labels={}
                        grafo_aux.indices=[]
                self.adyacencia_distritos[district] =[]
                print("Busqueda Ampliada correctamente")
    
    def ampliar_grafo(self,hospital_name):
        hospital_padre = self.labels[hospital_name]
        controlador = HospitalController()
        grafo_aux = GrafoHospitales()
        set_distritos_aux = list(self.distritos_recorridos)
        if len(set_distritos_aux) == 14:
            print("Busqueda amplificada al maximo. Ya no se puede expandir el area de busqueda")
        else:
            for district in set_distritos_aux: #recorriendo los distritos registrados en el set()
                
                adyacentes = self.adyacencia_distritos.get(district,[])#obteniendo los distritos adyacentes del diccionario de distritos
                for distrito in adyacentes:#recorriendo uno por uno los distritos
                    if distrito not in self.distritos_recorridos:#verificando si el distrito no fue añadido al set()
                        self.distritos_recorridos.add(distrito)#agregando el nuevo distrito al set
                        hospitales = controlador.get_hospitales_by_district(distrito)
                        grafo_aux.add_nodes(hospitales)
                        grafo_aux.crear_arista()
                        #definiendo el hospital del grafo auxiliar para aplicar el quick union al grafo principal
                        hospital_union = grafo_aux.nodos[0]
                        #Agregando los nodos y aristas del grafo auxiliar al grafo principal
                        self.nodos.extend(grafo_aux.nodos)
                        self.adyacencia.update(grafo_aux.adyacencia)
                        self.labels.update(grafo_aux.labels)
                        self.indices.extend(grafo_aux.indices)
                        self.quick_union(hospital_padre,hospital_union)
                        grafo_aux.nodos = []
                        grafo_aux.adyacencia = {}
                        grafo_aux.labels={}
                        grafo_aux.indices=[]
                self.adyacencia_distritos[district] =[]
                print("Busqueda Ampliada correctamente")


                


         


    