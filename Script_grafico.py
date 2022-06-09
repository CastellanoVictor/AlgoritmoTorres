from operator import index
import matplotlib.pyplot as plt
import random 
import math
import numpy as np 

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


    def getName(self):
        return(self.name) 

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

    #El método angul un nodo secundario y regresa el angulo con la horizontal entre ambos nodos.
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


    def ang_change(self, list_obj):
        #Las distanias y los angulos de los nodos secundarios respecto al nodo principal se ponen en arreglos
        dis_nod = [] #[self.distance(otherNode), self.distance(otherNode1), self.distance(otherNode2), self.distance(otherNode3)]
        disang_nod = [] #[self.angul(otherNode), self.angul(otherNode1), self.angul(otherNode2), self.angul(otherNode3)]
        name_nod = []
        weight_nod = []
        priority = []

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


        # print(name_nod)
        # print(disang_nod)
        # print(pr)

        vecdisn = []
        #Los vectores gen guardan los ángulos formados entre la horizontal y la recta que forman los nodos 
        gen = []
        gen1 = []
        gen2 = []
        gen3 = []

        #Los vectores mi guardan los indices respecto a los vectores principales (donde se guardan todas las 
        # posiciones). Esto indica que posición del arreglo disang_nod corresponde a qué ángulo respecto al
        #nodo principal.
        mi1 = []
        mi2 = []
        mi3 = []
        
        #En estos vectores simplemente asignamos la distancia más corta que corresponda según los ángulos 
        #en determinado rango del nodo principal.
        #Es decir, respecto a las posiciones guardadas en los arreglos mi, guardamos (por ejemplo) en a todas
        #las distancias de ese rango de angulos, que para el ejemplo es de 0 a 120.
        a = []
        b = []
        c = []

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
        
        #vecdisn.append(self.name)
        #En los siguentes tres bloques de codigo (es uno para cada rango) en los dos coindicionales se verifica
        #primertamente que no sean arreglos vacios para evitar errores, después agregamos las distancias 
        #correspondientes de cada nodo secundario. En otros terminos, clasifica las distancias de los demás 
        #nodos en función del rango en el que se encuentren.
        if mi1 != []:
            for i in mi1:
                if gen1 != []:
                    a.append(pr[i])

            #El arreglo gen es el que finalmente es devuelto por el método, por lo tanto regresa los siguientes datos:
            #A, B o C. Que es el rango en que el que se encuentra el nodo.
            #El mínimo valor del arreglo a, b o c. Que se trata del nodo más cercano para el rango en el que se esté.
            #El índice del arreglo de distancias de nuestro nodo más cercano.
            #El ángulo del índice mencionado anteriormente, para comprobar que esté en el rango. 
            vecdisn.append(disang_nod[int(pr.index(min(a)))])



        if mi2 != []:
            for i in mi2:
                if gen2 != []:
                    b.append(pr[i])
            vecdisn.append(disang_nod[int(pr.index(min(b)))])

        if mi3 != []:
            for i in mi3:
                if gen3 != []:
                    c.append(pr[i])
            vecdisn.append(disang_nod[int(pr.index(min(c)))])

        #vecdisn = list(reversed(vecdisn))
        return(vecdisn)

    #Esta función establece los parámetros de los posibles nodos secundarios a conectarse con el nodo principal
    def conection(self, list_obj):
        #Las distanias y los angulos de los nodos secundarios respecto al nodo principal se ponen en arreglos
        dis_nod = [] #[self.distance(otherNode), self.distance(otherNode1), self.distance(otherNode2), self.distance(otherNode3)]
        disang_nod = [] #[self.angul(otherNode), self.angul(otherNode1), self.angul(otherNode2), self.angul(otherNode3)]
        name_nod = []
        weight_nod = []
        priority = []

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


        # print(name_nod)
        # print(disang_nod)
        # print(pr)

        vecdisn = []
        #Los vectores gen guardan los ángulos formados entre la horizontal y la recta que forman los nodos 
        gen = []
        gen1 = []
        gen2 = []
        gen3 = []

        #Los vectores mi guardan los indices respecto a los vectores principales (donde se guardan todas las 
        # posiciones). Esto indica que posición del arreglo disang_nod corresponde a qué ángulo respecto al
        #nodo principal.
        mi1 = []
        mi2 = []
        mi3 = []
        
        #En estos vectores simplemente asignamos la distancia más corta que corresponda según los ángulos 
        #en determinado rango del nodo principal.
        #Es decir, respecto a las posiciones guardadas en los arreglos mi, guardamos (por ejemplo) en a todas
        #las distancias de ese rango de angulos, que para el ejemplo es de 0 a 120.
        a = []
        b = []
        c = []

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
        
        vecdisn.append(self.name)
        #En los siguentes tres bloques de codigo (es uno para cada rango) en los dos coindicionales se verifica
        #primertamente que no sean arreglos vacios para evitar errores, después agregamos las distancias 
        #correspondientes de cada nodo secundario. En otros terminos, clasifica las distancias de los demás 
        #nodos en función del rango en el que se encuentren.
        if mi1 != []:
            for i in mi1:
                if gen1 != []:
                    a.append(pr[i])

            #El arreglo gen es el que finalmente es devuelto por el método, por lo tanto regresa los siguientes datos:
            #A, B o C. Que es el rango en que el que se encuentra el nodo.
            #El mínimo valor del arreglo a, b o c. Que se trata del nodo más cercano para el rango en el que se esté.
            #El índice del arreglo de distancias de nuestro nodo más cercano.
            #El ángulo del índice mencionado anteriormente, para comprobar que esté en el rango. 
            vecdisn.append(name_nod[int(pr.index(min(a)))])

        if mi2 != []:
            for i in mi2:
                if gen2 != []:
                    b.append(pr[i])
            vecdisn.append(name_nod[int(pr.index(min(b)))])

        if mi3 != []:
            for i in mi3:
                if gen3 != []:
                    c.append(pr[i])
            vecdisn.append(name_nod[int(pr.index(min(c)))])

        return(vecdisn)


   


def plotter():
    

    #Establece la conección entre dos nodos indicados por sus coordenadas 
    #k es el numero del nodo principal
    #l es el numero del nodo con el que se compara 

    plt.plot(x, y, 'ro')

    for k in range(0, len(list_obj)):
        for l in range(1, len(list_obj)):
            if k < l:
                for r in range(0, len(list_obj[k].conection(list_obj))):
                    for t in range(0, len(list_obj[l].conection(list_obj))):
                        #print("Test 1 ", list_obj[k].conection(list_obj)[int(0)], list_obj[l].conection(list_obj)[int(t)])
                        #print("Test 2", list_obj[k].conection(list_obj)[int(r)], list_obj[l].conection(list_obj)[int(0)])
                        if list_obj[k].conection(list_obj)[int(0)] == list_obj[l].conection(list_obj)[int(t)] and list_obj[k].conection(list_obj)[int(r)] == list_obj[l].conection(list_obj)[int(0)]:

                            print(list_obj[k].conection(list_obj)[int(0)], list_obj[l].conection(list_obj)[int(0)], "conect")
                            print(list_obj[k].ang_change(list_obj)[r-1])

                            if list_obj[k].ang_change(list_obj)[r-1] >= 0 and list_obj[k].ang_change(list_obj)[r-1] <= 120:
                                list_obj[k].ang1 = list_obj[k].ang_change(list_obj)[r-1]
                                print()
                                print(list_obj[k].ang_change(list_obj)[int(0)])
                                print("Cambio de ang {} en pos {}".format(list_obj[k].name, list_obj[k].ang1))
                            if list_obj[k].ang_change(list_obj)[r-1] > 120 and list_obj[k].ang_change(list_obj)[r-1] <= 240:
                                list_obj[k].ang2 = list_obj[k].ang_change(list_obj)[r-1] 
                                print()
                                print(list_obj[k].ang_change(list_obj)[int(0)])
                                print("Cambio de ang {} en pos {}".format(list_obj[k].name, list_obj[k].ang2))
                            if list_obj[k].ang_change(list_obj)[r-1] > 240 and list_obj[k].ang_change(list_obj)[r-1] <= 360:
                                list_obj[k].ang3 = list_obj[k].ang_change(list_obj)[r-1]
                                print()
                                print(list_obj[k].ang_change(list_obj)[int(0)])
                                print("Cambio de ang {} en pos {}".format(list_obj[k].name, list_obj[k].ang3))

                            print(list_obj[l].conection(list_obj)[int(0)], list_obj[k].conection(list_obj)[int(0)])
                            print(list_obj[l].ang_change(list_obj)[t-1])

                            if list_obj[l].ang_change(list_obj)[t-1] >= 0 and list_obj[l].ang_change(list_obj)[t-1] <= 120:
                                list_obj[l].ang1 = list_obj[l].ang_change(list_obj)[t-1]
                                print()
                                print(list_obj[l].ang_change(list_obj)[int(0)])
                                print("Cambio de ang {} en pos {}".format(list_obj[l].name, list_obj[l].ang1))
                            if list_obj[l].ang_change(list_obj)[t-1] > 120 and list_obj[l].ang_change(list_obj)[t-1] <= 240:
                                list_obj[l].ang2 = list_obj[l].ang_change(list_obj)[t-1] 
                                print()
                                print(list_obj[l].ang_change(list_obj)[int(0)])
                                print("Cambio de ang {} en pos {}".format(list_obj[l].name, list_obj[l].ang2))
                            if list_obj[l].ang_change(list_obj)[t-1] > 240 and list_obj[l].ang_change(list_obj)[t-1] <= 360:
                                list_obj[l].ang3 = list_obj[l].ang_change(list_obj)[t-1]
                                print()
                                print(list_obj[l].ang_change(list_obj)[int(0)])
                                print("Cambio de ang {} en pos {}".format(list_obj[l].name, list_obj[l].ang3))


                            print()
                            plt.plot([list_obj[k].x, list_obj[l].x], [list_obj[k].y, list_obj[l].y])


    fig, ax = plt.subplots()
    ax.plot(x,y, ls="", marker="o")
    for xi, yi, pidi in zip(x,y,pid):
        ax.annotate(str(pidi), xy=(xi,yi))
    plt.axis([0, 100, 0, 100])
    plt.show()


def instace():
        for obj in list_obj:
            print()
            print("Soy el nodo {} y mi coordenada x {}, y: {}, los angulos {}, {}, {}, peso: {}".format(obj.name, obj.x, obj.y, obj.ang1, obj.ang2, obj.ang3, obj.weight))
            print(obj.conection(list_obj))
            print(obj.ang_change(list_obj))
            print()
            #print("Angulos de los demás nodos respecto a: ", obj.angul())

if __name__ == "__main__":

    n = int(input("Número de objetos: "))
    list_obj = []
    for i in range(int(n)):
        obj = Nodo(random.randint(1,100), random.randint(1,100), random.randint(1, 120), random.randint(121,240), random.randint(241, 360), "nodo[{}]".format(i), random.randint(5, 5))
        # Instancia un objeto con un elemento aleatorio de la lista colores
        list_obj.append(obj)
        
    instace()
    #print(obj.ang_change(list_obj))
    #Impresión de nodos
    pid = []
    for i in range (0, len(list_obj)):
        pid.append(i)
    x = []
    y = []
    for obj in list_obj:
        x.append(obj.x)
        y.append(obj.y)
        
    plotter()

    j = 0
    while True:
        print()
        #print(list_obj)
        opcion = int(input("Agregar nodo 1, Borrar Nodo 2, modificar peso 3, salir 4: "))
        if opcion == 1:
            j += 1
            list_obj.append(Nodo(random.randint(1,100), random.randint(1,100), random.randint(1, 120), random.randint(121,240), random.randint(241, 360), "nodo[{}]".format(i + j), random.randint(5, 5)))
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
        pid = []
        for i in range(0, len(list_obj)):
            pid.append(i)

        x = []
        y = []
        for obj in list_obj:
            x.append(obj.x)
            y.append(obj.y)
        
        plotter()
