import copy

FALLO = 'FALLO'
EXITO = 'EXITO'
DEBUG = False

def debug(msg):
    if DEBUG:
        print(msg)
    else:
        pass

class Nodo:
    
    def __init__(self,antecesor,sucesores,profundidad,heuristica,funcion_ev):
        self.antecesor = antecesor
        self.sucesores = sucesores
        self.profundidad = profundidad  # g
        self.heuristica = heuristica    # h
        self.funcion_ev = funcion_ev    # f

    def __str__(self):
        message = """Profundidad = {}
Heuristica = {}
Funcion de Evaluacion = {}""".format(self.profundidad,self.heuristica,self.funcion_ev)
        return message

    def __eq__(self, nodo):
        # Se implementa en cada problema para comprobar estados iguales
        pass

    def tiene_como_ascendiente(self,posible_sucesor):
        """
        Comprueba si el nodo posible_sucesor está entre los ascendientes 
        del propio Nodo.
        Necesita implementar el método __eq__ de las clases que hereden de Nodo
        """
        nodo = copy.copy(self)
        while nodo.antecesor:
            if nodo.antecesor == posible_sucesor:
                return True
            nodo = nodo.antecesor
        return False

    def generar_sucesores_no_ascendientes(self, **kwargs):
        # Implementar segun el problema
        pass
        
    def reconsiderar_apuntador(self,nuevo_nodo):
        # Implementar según la función de evaluación
        pass

    def devolver_camino(self):
        # Devuelve una lista desde el nodo inicial hasta el nodo que ejecuta el metodo
        camino = []
        nodo = copy.copy(self)
        camino.append(nodo)
        while nodo.antecesor:
            camino.append(nodo.antecesor)
            nodo = nodo.antecesor
        return camino[::-1] # a la inversa para empezar por el nodo inicial


class Grafo:

    def __init__(self,nodo_inicial):
        self.abiertos = None
        self.cerrados = None
        self.nodo_inicial = nodo_inicial 

    # Linea 5
    def es_nodo_objetivo(self,nodo):
        # Implementar según el problema
        pass

    # Lineas 6-7
    def expandir_nodo(self,nodo,**kwargs):
        """
        Establecer apuntador a n en los sucesores que no esten en abiertos o cerrados
            Si aparecian, considerar modificar apuntador hacia n
        Cada miembro en cerrados, decidir si modificar los apuntadores de sus descendientes
        """
        nodo.generar_sucesores_no_ascendientes(**kwargs) # Linea 6
        for sucesor in nodo.sucesores:
            if sucesor in self.abiertos:
                # reconsiderar apuntador del nodo en abiertos
                for n in self.abiertos:
                    if n == nodo:
                        n.reconsiderar_apuntador(nodo)
                        break
            elif sucesor in self.cerrados:
                # reconsiderar apuntador del nodo en cerrados
                for n in self.cerrados:
                    if n == nodo:
                        n.reconsiderar_apuntador(nodo)
                        #tambien el de los sucesores
            else:
                sucesor.antecesor = copy.copy(nodo)
                self.abiertos.append(sucesor) #estado nuevo

    def iniciar_A_estrella(self,**kwargs):
        """
        kwargs representa la información extra del problema que se pueda tener que
        proporcionar, por ejemplo, para generar sucesores o comprobar si es objetivo
        """
        # Linea 1
        self.abiertos = [self.nodo_inicial]
        
        # Linea 2
        self.cerrados = []
        
        # Linea 3 y 9
        while(True):
            debug("\n############################## NUEVO NODO DE ABIERTOS ###################################")
            debug("ABIERTOS: {}\nCERRADOS: {}".format(self.abiertos,self.cerrados))
            debug("Compruebo si abiertos está vacía")
            if len(self.abiertos) == 0:
                debug("Lo está")
                return FALLO
            debug("No lo está")
            # Linea 4
            n = self.abiertos.pop(0) 
            self.cerrados.append(n)
            debug("Saco este nodo de abiertos y lo meto a cerrados\n{}".format(n))
            # Linea 5
            debug("Compruebo si es objetivo:")
            if self.es_nodo_objetivo(n):
                debug("Es objetivo")
                grafo = n.devolver_camino()
                debug("Camino de longitud: {}".format(len(grafo)))
                return grafo  # EXITO
            debug("No es objetivo")
            # Lineas 6-7
            debug("Expando el nodo.")
            self.expandir_nodo(n,**kwargs)
            debug("--- Nodos sucesores ---")
            for s in n.sucesores:
                debug(s.nombre)
            debug("-----------------------")
            # Linea 8
            debug("Ordeno abiertos")
            self.abiertos.sort(key=lambda nodo: nodo.funcion_ev)
            debug("############################### FIN NODO DE ABIERTOS ####################################\n")


            
            



