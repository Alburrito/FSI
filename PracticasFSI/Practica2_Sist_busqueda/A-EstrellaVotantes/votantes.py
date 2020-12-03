import csv
import sys,argparse
from a_star import *

DEFAULT_RUTA_CONTACTOS = 'resources/contactos.csv'
MENSAJE_DESCRIPCION = "Muestra, si la hay, la ruta ideologica entre dos contactos, aportando la carga ideologica inicial de uno de ellos"
AYUDA_LISTA_CONTACTOS = "Ruta al fichero .csv donde se encuentran los contactos y su factor K correspondiente. Por defecto: contactos.csv"
AYUDA_VOTANTE_INICIAL = "OBLIGATORIO. Nombre del votante del que se parte. Debe estar en la lista de contactos proporcionada"
AYUDA_CARGA_IDEOLOGICA = "OBLIGATORIO. Carga ideologica del votante inicial. Debe ser un numero positivo"
AYUDA_VOTANTE_OBJETIVO = "OBLIGATORIO. Nombre del votante al que se quiere llegar a convencer. Si no está en la lista o no hay ruta posible se obtendrá un FALLO"

# Implementa particularidades del problema para el Nodo
class Votante(Nodo):

    def __init__(self, nombre, carga_ideologica, antecesor,sucesores,profundidad,heuristica,funcion_ev):
        self.nombre = nombre
        self.carga_ideologica = carga_ideologica
        super().__init__(antecesor,sucesores,profundidad,heuristica,funcion_ev)

    def __str__(self):
        message ="\n============ NODO ===========\n"
        message += """Nombre = {}
Carga Ideologica = {}""".format(self.nombre, self.carga_ideologica)
        message +="\n---------------------------\n"
        message += super().__str__()
        message +="\n============================"
        return message

    def __eq__(self, votante):
        return self.nombre == votante.nombre

    def generar_sucesor_valido(self,nombre,factorK):
        """
        Si el Votante que ejecuta el metodo convence al votante proporcionado se
        devuelve el objeto Votante correspondiente al sucesor.
        Si no lo convence, se devuelve None
        Comprueba también, usando el método de la clase padre Nodo, que no sea ascendiente.
        """
        if self.carga_ideologica > 0.09:
            carga_ideologica = round(self.carga_ideologica * float(factorK),2)
            if carga_ideologica > 0.09:
                antecesor = None
                sucesores = None
                profundidad = self.profundidad + 1
                heuristica = carga_ideologica
                funcion_ev = round(heuristica - profundidad,2) # h - g. Cuanto más alta mejor
                # TODO: posible cambio:
                #   + contactos => mejor
                #   + factorK   => mejor
                # Buscar formula de punto medio?
                votante = Votante(nombre,carga_ideologica,antecesor,sucesores,profundidad,heuristica,funcion_ev)
                if not self.tiene_como_ascendiente(votante):
                    return votante

        return None

    # Override
    def generar_sucesores_no_ascendientes(self,**kwargs):
        # Establece self.sucesores como una lista de los sucesores del propio votante
        # que no sean ascendientes del mismo
        if 'contactos' in kwargs.keys():
            sucesores = []
            for contacto in kwargs['contactos']:
                if self.nombre in contacto:
                    factorK = contacto[2]
                    if contacto.index(self.nombre) == 0:
                        nombre = contacto[1]
                    else:
                        nombre = contacto[0]
                    sucesor = self.generar_sucesor_valido(nombre,factorK)
                    if sucesor:
                        sucesores.append(sucesor)
            self.sucesores = sucesores    
        
    # Override
    def reconsiderar_apuntador(self,nuevo_nodo):
        if nuevo_nodo.funcion_ev > self.funcion_ev:
            self.antecesor = nuevo_nodo.antecesor
            self.profundidad = nuevo_nodo
            self.funcion_ev = self.funcion_ev

# Implementa particularidades del problema para el Grafo
class RutaIdeologica(Grafo):

    def __init__(self,votante_convencido,votante_a_convencer,ruta_contactos):
        """
        (votante_convencido : Votante) Nodo inicial desde el que se parte
        (votante_a_convencer : Votante) Nodo al que se quiere llegar
        (ruta_contactos : str) Ruta al fichero csv que contiene la lista de contactos (nombre1, nombre2, factorK)
        """
        super().__init__(votante_convencido)
        #self.votante_convencido = votante_convencido
        self.votante_a_convencer = votante_a_convencer
        self.ruta_contactos = ruta_contactos
        self.contactos = self.leer_contactos(ruta_contactos) # Lista de contactos. Se lee de un fichero
        self.ruta_optima = None # Ruta optima desde el primer votante hasta el votante objetivo

    # Override
    def es_nodo_objetivo(self,nodo):
        """
        Comprueba si el Votante correspondiente al nodo comprobado es el mismo que
        el votante_a_convencer

        (nodo : Votante) nodo que se quiere comprobar
        """
        if nodo.nombre == self.votante_a_convencer.nombre:
            return True
        return False

    def leer_contactos(self,ruta_fichero):
        contactos = []
        with open(ruta_fichero,'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for contacto in csv_reader:
                contactos.append(tuple(contacto))
        return contactos

    def comprobar_validez(self):
        """
        Comprueba que existan tanto el estado inicial como el final
        La variable 'resultado' vale:
            · 0 si no encontró ninguno
            · 1 si encontró solo el inicial
            · 2 si encontró solo el final
            · 3 si encontró ambos => Problema valido
        """
        resultado = 0
        inicial_encontrado = False
        objetivo_encontrado = False

        for contacto in self.contactos:
            if not inicial_encontrado and self.nodo_inicial.nombre in contacto:
                resultado += 1
                inicial_encontrado = True
            if not objetivo_encontrado and self.votante_a_convencer.nombre in contacto:
                resultado +=2
                objetivo_encontrado = True
            if inicial_encontrado and objetivo_encontrado:
                break

        if resultado < 3:
            print("FALLO EN LOS NOMBRES PROPORCIONADOS:")
            if resultado == 0:
                print("No se pudo encontrar a ninguno de los votantes ({} y {}) en la lista de contactos {}".format(self.nodo_inicial.nombre,
                                                                                                                    self.votante_a_convencer.nombre,
                                                                                                                    self.ruta_contactos))
            elif resultado == 1:
                print("No se pudo encontrar al votante objetivo {} en la lista de contactos {}".format(self.votante_a_convencer.nombre,
                                                                                                        self.ruta_contactos))
            elif resultado == 2:
                print("No se pudo encontrar al votante inicial {} en la lista de contactos {}".format(self.nodo_inicial.nombre,
                                                                                                        self.ruta_contactos))
            print("Saliendo...")
            sys.exit()

    def calcular_ruta_optima(self):
        print("=====================================================================")
        print("Calculando ruta optima desde: ",end='')
        print("Votante {} con carga ideologica {}".format(self.nodo_inicial.nombre, self.nodo_inicial.carga_ideologica))
        print("Hasta: Votante {} con carga ideologica > 0.09".format(self.votante_a_convencer.nombre))
        self.comprobar_validez()
        self.ruta_optima = self.iniciar_A_estrella(contactos=self.contactos) # Heredado de Grafo
        print("Ruta calculada.")
        print("=====================================================================")

    def imprimir_ruta_optima(self):
        print("=====================================================================")
        if self.ruta_optima != FALLO:    
            print("Imprimiendo ruta...")
            for votante in self.ruta_optima:
                print("Nombre: {}\tCarga Ideologica: {}".format(votante.nombre,votante.carga_ideologica))
            print("Ruta impresa. Nº conactos: {}".format(len(self.ruta_optima)-1))
        else:
            print("No se encontró una ruta")
        print("=====================================================================")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=MENSAJE_DESCRIPCION)
    parser.add_argument('votante_inicial',type=str, help=AYUDA_VOTANTE_INICIAL)
    parser.add_argument('carga_ideologica',type=float, help=AYUDA_CARGA_IDEOLOGICA)
    parser.add_argument('votante_objetivo',type=str, help=AYUDA_VOTANTE_OBJETIVO)
    parser.add_argument('-f', type=str, help=AYUDA_LISTA_CONTACTOS, default=DEFAULT_RUTA_CONTACTOS, metavar='RUTA_CONTACTOS')
    args = parser.parse_args()

    # Votante inicial
    v1 = Votante(args.votante_inicial,args.carga_ideologica,None,None,0,0,0)
    # Votante objetivo
    v2 = Votante(args.votante_objetivo,None,None,None,None,None,None)
    rI = RutaIdeologica(v1,v2,args.f)
    rI.calcular_ruta_optima()
    rI.imprimir_ruta_optima()