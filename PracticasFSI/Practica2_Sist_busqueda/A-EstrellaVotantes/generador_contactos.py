import csv
import random
import sys
import argparse

DEFAULT_NUM_CONTACTOS = 50
DEFAULT_RUTA_NOMBRES = 'resources/nombres.txt'
DEFAULT_RUTA_CONTACTOS = 'resources/contactos.csv'

MENSAJE_DESCRIPCION = "Pequeño script que lee un listado de nombres y genera otro con contactos aleatorios.\n"
MENSAJE_DESCRIPCION += "Estos contactos se componen de (nombre1, nombre2, fortaleza).\n"
MENSAJE_DESCRIPCION += "La lista de contactos se guardará en la ruta especificada (por defecto, 'resources/contactos.csv.\n"
MENSAJE_DESCRIPCION += "Es posible instanciar la clase Generador y llamar al método generar_contactos() para crear la lista y al método get_contactos() para recuperarla\n"
MENSAJE_DESCRIPCION += "Álvaro Martín López - almarlop98@gmail.com\nGithub: Alburrito."

class Generador:

    def __init__(self, num_contactos=None, ruta_nombres=None,ruta_contactos=None):
        self.num_contactos = num_contactos
        self.ruta_nombres = ruta_nombres
        self.ruta_contactos = ruta_contactos
        self.nombres = []
        self.contactos = []

    def cargar_nombres(self):
        print("Cargando nombres de {}...".format(self.ruta_nombres))
        with open(self.ruta_nombres,'r') as nombres:
            csv_reader = csv.reader(nombres, delimiter='\n')
            for nombre in csv_reader:
                self.nombres.append(nombre[0])
        print("Hecho: {} nombres cargados".format(len(self.nombres)))
        
    def guardar_contactos(self):
        print("Guardando contactos...")
        with open(self.ruta_contactos,'w') as contactos:
            csv_writer = csv.writer(contactos)
            for c in self.contactos:
                csv_writer.writerow(c)
        print("Hecho: Contactos guardados en {}".format(self.ruta_contactos))

    def generar_contactos(self):
        self.cargar_nombres()
        i = 1
        print("Generando {} contactos aleatorios...".format(self.num_contactos))
        while i <= self.num_contactos:
            found = True
            while found:
                found = False
                # Generar nombres
                n1 = random.choice(self.nombres)
                n2 = random.choice(self.nombres)
                while n2 == n1:
                    n2 = random.choice(self.nombres)
                # Comprobar contacto no repetido
                for c in self.contactos:
                    if n1 in c and n2 in c:
                        found = True
                        break
                if found:
                    continue      
                # Generar fortaleza, factorK
                temp = random.randint(0,2)
                if temp == 0: # se llevan mal
                    factorK = random.random()
                else: # se llevan bien
                    factorK = random.uniform(1.0,4.0)
                factorK = round(factorK,2)
                contacto = [n1,n2,str(factorK)]
            self.contactos.append(contacto)
            i +=1
        print("Hecho: {} contactos generados".format(len(self.contactos)))
        if self.ruta_contactos:
            self.guardar_contactos()

    def get_contactos(self):
        return self.contactos



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=MENSAJE_DESCRIPCION)
    parser.add_argument('-nc', type=int, help="Numero de contactos generados",
                        default=DEFAULT_NUM_CONTACTOS,
                        metavar='NUM_CONTACTOS')
    parser.add_argument('-n', type=str, help="Ruta al fichero con nombres. Uno por linea. Si no se especifica es 'nombres.txt'",
                        default=DEFAULT_RUTA_NOMBRES,
                        metavar='RUTA_NOMBRES')
    parser.add_argument('-c', type=str, help="Ruta donde se guardará el fichero de contactos, si se quiere guardar en fichero.\n"
                                            +"Por defecto se guardará en 'resources/contactos.csv\n",
                        default=DEFAULT_RUTA_CONTACTOS,
                        metavar='RUTA_CONTACTOS')
    
    args = parser.parse_args()
    num_contactos = args.nc
    ruta_nombres = args.n
    ruta_contactos = args.c

    if len(sys.argv) == 1:
        print("=====================================================================")
        print("EJECUTANDO SIN ARGUMENTOS")
        print("Generando {} contactos a partir de {}.\nExportando a {}".format(num_contactos, ruta_nombres,ruta_contactos))
        print("Ejecutar 'python3 generador_contactos.py -h' para mas informacion")
        print("=====================================================================")

    g = Generador(num_contactos, ruta_nombres, ruta_contactos)
    g.generar_contactos()