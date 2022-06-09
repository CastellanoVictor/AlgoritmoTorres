#import matplotlib.pyplot as plt
import random 
import math
import numpy as np 
from pyproj import Transformer
from pyproj import CRS


class Nodo:
    #Se incluyen los atributos de la clase nodo
    def __init__(self, x, y, ang1, ang2, ang3, name, weight):
        self.x = x
        self.y = y
        self.ang1 = ang1
        self.ang2 = ang2
        self.ang3 = ang3
        self.name = name
        self.weight = weight

    #Nombre del nodo, será usado como identificador 
    def getName(self):
        return(self.name) 

    #El peso será usado para alterar las conexiones entre nodos en función de la distancia
    def getWeight(self):
        return(self.weight)
 
    #Coordenadas de un nodo
    def getCoordinates(self):
        return([self.x, self.y])
    
    #Retorno los ángulos de cada rango de antenas de un nodo
    def getAngles(self):
        return([self.ang1, self.ang2, self.ang3])

    #Distancia total entre dos nodos 
    def distance(self, otherNode):
        x_diff = (self.x - otherNode.x)**2
        y_diff = (self.y - otherNode.y)**2
        return((x_diff + y_diff)**0.5)

    #Distancia entre dos nodos en el plano X
    def distancex(self, otherNode):
        return(self.x - otherNode.x)

    #Distancia entre dos nodos en el plano Y
    def distancey(self, otherNode):
        return(self.y - otherNode.y)

    #El método angul recibe un nodo secundario y regresa el angulo formado entre la horizontal 
    #entre la línea que forman ambos nodos.
    ''''
    Se plantean cuatro posibles casos, de a cuerdo a donde esté el ángulo secundario respecto al ángulo principal
    los cálculos se hicieron de acuerdo a geometría. 
    Se convierte a grados cada ángulo y al final, se regresa. Es importante señalar el ángulo que se devuelve es 
    respecto a la horizontal.
    '''
    def angul(self, otherNode):
        theta = 0
        if self.x <= otherNode.x and self.y <= otherNode.y:
            if self.distance(otherNode) != 0:
                theta = math.acos(abs(self.distancex(otherNode))/abs(self.distance(otherNode)))*57.2958
        elif self.x >= otherNode.x and self.y <= otherNode.y:
            if self.distance(otherNode) != 0:
                theta = 180 - math.acos(abs(self.distancex(otherNode))/abs(self.distance(otherNode)))*57.2958
        elif self.x >= otherNode.x and self.y >= otherNode.y:
            if self.distance(otherNode) != 0:
                theta = 180 + math.acos(abs(self.distancex(otherNode))/abs(self.distance(otherNode)))*57.2958
        elif self.x <= otherNode.x and self.y >= otherNode.y:
            if self.distance(otherNode) != 0:
                theta = 360 - math.acos(abs(self.distancex(otherNode))/abs(self.distance(otherNode)))*57.2958
        return(theta)


    """
    La función devuelve una lista de ángulos, corresponden a cada antena de la torre y dirigen al nodo
    más factible a conectar, de a cuerdo con el arreglo a distancia y peso.
    """
    def ang_change(self, list_obj):
        #Características de otro nodo respecto al nodo con el que se desea sacar el ángulo 
        dis_nod = [] 
        disang_nod = [] 
        name_nod = []
        weight_nod = []
        priority = []
        priority_angles = []

        #Los vectores gen guardan todos los ángulos formados entre la horizontal y la recta que forman 
        # los nodos pero clasificados respecto a en qué antena de la torre (nodo) podrían ser conectados
        gen1 = []
        gen2 = []
        gen3 = []

        #Los vectores mi guardan los indices respecto a los vectores principales (donde se guardan todas las 
        # posiciones). Esto indica que posición del arreglo disang_nod corresponde a qué ángulo respecto al
        # nodo principal.
        mi1 = []
        mi2 = []
        mi3 = []
        
        #En estos vectores simplemente asignamos la prioridad más corta que corresponda según los ángulos 
        #en determinado rango del nodo principal.
        #Es decir, respecto a las posiciones guardadas en los arreglos mi, guardamos (por ejemplo) en a todas
        #las distancias de ese rango de angulos, que para el ejemplo es de 0 a 120.
        a = []
        b = []
        c = []

        #Se alimentan los arreglos con los métodos y atributos del mismo nodo respecto a con que se compara
        for obj in list_obj:
            dis_nod.append(self.distance(obj))
            disang_nod.append(self.angul(obj))
            name_nod.append(obj.getName())
            weight_nod.append(obj.weight)

        #En todos los arreglos quedará un índice nulo, que es de comprar al nodo consigo mismo 
        dis_nod.remove(0.0)
        disang_nod.remove(0)   
        name_nod.remove(self.name)
        weight_nod.remove(self.weight)

        #Priority es el arreglo entre la distancia y el peso para definir como deben conectarse los
        #nodos además de sus restricciones fisicas y geográficas.
        priority = np.array(dis_nod)/np.array(weight_nod)
        pr = list(priority)


        #Este cliclo comprueba en que rango del nodo principal se encuentran los demás nodos en base a los 
        #angulos obtenidos en pasos anteriores.
        for i in range(0, len(dis_nod)):
            if disang_nod[i] >= 0 and disang_nod[i] <= 120:
                gen1.append(disang_nod[i])
                mi1.append(i)
            elif disang_nod[i] > 120 and disang_nod[i] <= 240:
                gen2.append(disang_nod[i])
                mi2.append(i)
            elif disang_nod[i] > 240 and disang_nod[i] <= 360:
                gen3.append(disang_nod[i])
                mi3.append(i)

            """
            En los siguentes tres bloques de codigo (es uno para cada rango) en los dos coindicionales se verifica
            primertamente que no sean arreglos vacios para evitar errores, después agregamos las distancias 
            correspondientes de cada nodo secundario. En otros terminos, clasifica las distancias de los demás 
            nodos en función del rango en el que se encuentren.
            """

            """
            Como ya se explicó, en los arrelgos a, b, c se guardan los índices del nodo más viable a 
            conectar en esa antena del nodo en base a Priority, que es el arreglo entre distancia y
            peso.
            Finalmente, con este índice, tomaremos el mínimo y lo ubicamos en las prioridades, con lo
            que asignamos ese ángulo a la lista que retornará esta función.
            El proceso es iterativo para las tres antenas del cada torres.
            """

        if mi1 != []:
            for i in mi1:
                if gen1 != []:
                    a.append(pr[i])
            priority_angles.append(disang_nod[int(pr.index(min(a)))])

        if mi2 != []:
            for i in mi2:
                if gen2 != []:
                    b.append(pr[i])
            priority_angles.append(disang_nod[int(pr.index(min(b)))])

        if mi3 != []:
            for i in mi3:
                if gen3 != []:
                    c.append(pr[i])
            priority_angles.append(disang_nod[int(pr.index(min(c)))])

        return(priority_angles)

    """
    La función es bastante similar a la anterior, el proceso es el mismo, por lo tanto se evitó poner
    la documentación pues sería redundante explicar muchas de las funciones.
    Esta función regresa una arreglo con los posibles nodos a conectarse en sus respectivos rangos e 
    igualmente en orden, sin embargo, su primer elemento siempre será el nombre o identificador del
    mismo nodo, esto será útil al buscar los nodos que se deben conectar.
    """
    def name_change(self, list_obj):
        dis_nod = [] 
        disang_nod = [] 
        name_nod = []
        weight_nod = []
        priority = []
        priority_names = []

        gen1 = []
        gen2 = []
        gen3 = []

        mi1 = []
        mi2 = []
        mi3 = []
        
        a = []
        b = []
        c = []

        for obj in list_obj:
            dis_nod.append(self.distance(obj))
            disang_nod.append(self.angul(obj))
            name_nod.append(obj.getName())
            weight_nod.append(obj.weight)
        
        dis_nod.remove(0.0)
        disang_nod.remove(0)   
        name_nod.remove(self.name)
        weight_nod.remove(self.weight)

        priority = np.array(dis_nod)/np.array(weight_nod)
        pr = list(priority)


        for i in range(0, len(dis_nod)):
            if disang_nod[i] >= 0 and disang_nod[i] <= 120:
                gen1.append(disang_nod[i])
                mi1.append(i)
            elif disang_nod[i] > 120 and disang_nod[i] <= 240:
                gen2.append(disang_nod[i])
                mi2.append(i)
            elif disang_nod[i] > 240 and disang_nod[i] <= 360:
                gen3.append(disang_nod[i])
                mi3.append(i)
        
        #Como se mencionó en la descripción de la función, el primer elemento del arreglo de salida 
        # siempre será el del mismo nodo.
        priority_names.append(self.name)

        #Estos tres condicionales difieren con la funcion anterior en que no agregan los angulos sino
        #los nombres
        if mi1 != []:
            for i in mi1:
                if gen1 != []:
                    a.append(pr[i])
            priority_names.append(name_nod[int(pr.index(min(a)))])

        if mi2 != []:
            for i in mi2:
                if gen2 != []:
                    b.append(pr[i])
            priority_names.append(name_nod[int(pr.index(min(b)))])

        if mi3 != []:
            for i in mi3:
                if gen3 != []:
                    c.append(pr[i])
            priority_names.append(name_nod[int(pr.index(min(c)))])

        return(priority_names)


"""
Esta función analiza cada par de nodos en el conjunto total, y, si alguno se encuentra en la lista 
de conexiones posibles del nodo con el que se empareja, se establece una conexion.
Los primeros dos bucles recorren todos los nodos, los dos internos reccorren los elementos de cada nodo
que para efectos prácticos son los nodos con los que se pueden conectar.
"""
def conection():
    



    # plt.plot(x, y, 'ro')

    for k in range(0, len(list_obj)):     #k es el numero del nodo principal
        for l in range(1, len(list_obj)):    #l es el numero del nodo con el que se compara 
            if k < l:   #Evita comparar dos veces el mismo par de nodos.
                for r in range(0, len(list_obj[k].name_change(list_obj))):  #Elementos del nodo k
                    for t in range(0, len(list_obj[l].name_change(list_obj))):  #Elementos del nodo l

                        """
                        Esta línea compara el primer elemento de cada uno de los nodos con todos los
                        demás del otro nodo, para segurar que el primero de cada uno está en algún
                        índice del otro, para poder así establecer la conexion solo si se cumple este
                        condicional.
                        """
                        if list_obj[k].name_change(list_obj)[int(0)] == list_obj[l].name_change(list_obj)[int(t)] and list_obj[k].conection(list_obj)[int(r)] == list_obj[l].conection(list_obj)[int(0)]:
                            
                            print("Conect")     #Badera de coneccion
                            #Identificador de los nodos a conectar
                            print(list_obj[k].name_change(list_obj)[int(0)], list_obj[l].name_change(list_obj)[int(0)])
                            #Angulo del primer nodo para conectarse con el otro.
                            print(list_obj[k].ang_change(list_obj)[r-1])

                            """
                            En función de que angulo se requiera cambiar, se asignará a ese rango del nodo en cuestión.
                            Se comprobará en un arreglo de ifs parecido al que se hizo anteriormente y posteriormente se 
                            asigna.
                            """
                            if list_obj[k].ang_change(list_obj)[r-1] >= 0 and list_obj[k].ang_change(list_obj)[r-1] <= 120:
                                list_obj[k].ang1 = list_obj[k].ang_change(list_obj)[r-1]
                                print("Cambio en nodo {} a ang {}".format(list_obj[k].name, list_obj[k].ang1))
                                
                            if list_obj[k].ang_change(list_obj)[r-1] > 120 and list_obj[k].ang_change(list_obj)[r-1] <= 240:
                                list_obj[k].ang2 = list_obj[k].ang_change(list_obj)[r-1] 
                                print("Cambio en nodo {} a ang {}".format(list_obj[k].name, list_obj[k].ang2))
                                
                            if list_obj[k].ang_change(list_obj)[r-1] > 240 and list_obj[k].ang_change(list_obj)[r-1] <= 360:
                                list_obj[k].ang3 = list_obj[k].ang_change(list_obj)[r-1]
                                print("Cambio en nodo {} a ang {}".format(list_obj[k].name, list_obj[k].ang3))

                            
                            """
                            Se repite el mismo proceso para el nodo l que para el nodo k, pues ambos nodos deberán ser
                            orientados pero en diferentes direcciones.
                            """
                            print(list_obj[l].name_change(list_obj)[int(0)], list_obj[k].name_change(list_obj)[int(0)])
                            print(list_obj[l].ang_change(list_obj)[t-1])

                            if list_obj[l].ang_change(list_obj)[t-1] >= 0 and list_obj[l].ang_change(list_obj)[t-1] <= 120:
                                list_obj[l].ang1 = list_obj[l].ang_change(list_obj)[t-1]
                                print("Cambio en nodo {} a ang {}".format(list_obj[l].name, list_obj[l].ang1))

                            if list_obj[l].ang_change(list_obj)[t-1] > 120 and list_obj[l].ang_change(list_obj)[t-1] <= 240:
                                list_obj[l].ang2 = list_obj[l].ang_change(list_obj)[t-1] 
                                print("Cambio en nodo {} a ang {}".format(list_obj[l].name, list_obj[l].ang2))
                
                            if list_obj[l].ang_change(list_obj)[t-1] > 240 and list_obj[l].ang_change(list_obj)[t-1] <= 360:
                                list_obj[l].ang3 = list_obj[l].ang_change(list_obj)[t-1]
                                print("Cambio en nodo {} a ang {}".format(list_obj[l].name, list_obj[l].ang3))
                                


                            print()
                            # plt.plot([list_obj[k].x, list_obj[l].x], [list_obj[k].y, list_obj[l].y])


    # fig, ax = plt.subplots()
    # ax.plot(x,y, ls="", marker="o")
    # for xi, yi, pidi in zip(x,y,pid):
    #     ax.annotate(str(pidi), xy=(xi,yi))
    # plt.axis([0, 100, 0, 100])
    # plt.show()

"""
Esta función imprime las características principales del nodo así como sus nodos a conectar.
"""
def instace():
        for obj in list_obj:
            print()
            print("Soy el nodo {}, coor x: {}, y: {}, angulos: {}, {}, {}, peso: {}".format(obj.name, obj.x, obj.y, obj.ang1, obj.ang2, obj.ang3, obj.weight))
            print(obj.name_change(list_obj))
            print(obj.ang_change(list_obj))
            print()


"""
Esta función regresa en UTM una coordenada a partir de geográficas al azar.
"""
def coord():
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:26917", always_xy=True)
    crs_4326 = CRS.from_epsg(4326)
    crs_26917 = CRS.from_epsg(26917)
    transformer = Transformer.from_crs(crs_4326, crs_26917)
    transformer = Transformer.from_crs(4326, 26917)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:26917", always_xy=True)
    
    return(list(transformer.transform(random.randrange(-180, 180), random.randrange(-90, 90))))


if __name__ == "__main__":

    #Se instancian y guardan en una lista todos los objetos.
    n = int(input("Número de objetos: ")) 
    list_obj = []
    for i in range(int(n)):
        obj = Nodo(coord()[0], coord()[1], random.randint(1, 120), random.randint(121,240), random.randint(241, 360), "nodo[{}]".format(i), random.randint(5, 5))
        list_obj.append(obj)
    instace()

    #Impresión de nodos
    # pid = []
    # for i in range (0, len(list_obj)):
    #     pid.append(i)
    # x = []
    # y = []
    # for obj in list_obj:
    #     x.append(obj.x)
    #     y.append(obj.y)
        
    conection()

    j = 0 #Bandera para aumentar el número de los nodos.
    """
    Cilo que contiene menú para manipular el esquema de nodos.
    """
    while True:
        print()
        #print(list_obj)
        opcion = int(input("Agregar nodo 1, Borrar Nodo 2, modificar peso 3, salir 4: "))
        if opcion == 1:
            j += 1
            list_obj.append(Nodo(coord()[0], coord()[1], random.randint(1, 120), random.randint(121,240), random.randint(241, 360), "nodo[{}]".format(i + j), random.randint(5, 5)))
            j -= 1
        
        elif opcion == 2:
            list_obj.pop(len(list_obj)-1)
        
        elif opcion == 3:
            opcion2 = int(input("Nodo del cual se desea cambiar el peso: "))
            new_weight = int(input("Nuevo peso del nodo: "))
            list_obj[opcion2].weight = new_weight
        
        elif opcion == 4:
            break
        
        instace()

        #Impresión de nodos
        # pid = []
        # for i in range(0, len(list_obj)):
        #     pid.append(i)

        # x = []
        # y = []
        # for obj in list_obj:
        #     x.append(obj.x)
        #     y.append(obj.y)
        
        conection()
