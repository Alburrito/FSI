import generador_contactos
import votantes

num_contactos = 50
ruta_nombres = 'resources/nombres.txt'
ruta_contactos = 'resources/contactos.csv'
nombre1 = 'alvaro'
nombre2 = 'manolo'
cI = 0.5

g = generador_contactos.Generador(num_contactos, ruta_nombres, ruta_contactos)
g.generar_contactos()

# Votante inicial
v1 = votantes.Votante(nombre1,cI,None,None,0,0,0)
# Votante objetivo
v2 = votantes.Votante(nombre2,None,None,None,None,None,None)
rI = votantes.RutaIdeologica(v1,v2,ruta_contactos)
rI.calcular_ruta_optima()
rI.imprimir_ruta_optima()