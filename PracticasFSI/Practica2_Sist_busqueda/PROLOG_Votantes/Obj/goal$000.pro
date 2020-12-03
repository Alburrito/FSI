/*****************************************************************************

		Copyright (c) My Company

 Project:  PRACTICA
 FileName: PRACTICA.PRO
 Purpose: No description
 Written by: Visual Prolog
 Comments:
******************************************************************************/

include "practica.inc"

domains
	limite=integer
	nombre=symbol
	cargaIdeologica=real
	factorK=real
	votante=v(nombre,cargaIdeologica)
	lista=votante*
	
predicates
	contacto(nombre,nombre,factorK)
	convence(votante,votante)		
	miembro(votante,lista)
	rutaIdeologica(votante,votante,lista,lista,limite,limite)
	pinta(lista)
	
  practica()

clauses

/* Alguna forma?
	contacto(A,B,_):-		
		contacto(B,A,_).
*/

	/* Lista contacto */
	contacto(pepe,juan,0.3).
	contacto(juan,manolo,0.6).
	contacto(manolo,luis,4.0).
	contacto(josemari,lucia,4.0).
	contacto(raul,josemari,3.0).
	contacto(luis,felipe,2.0).
	contacto(manolo,felipe,2.5).
	contacto(pepe,vidal,1.0).
	contacto(pepe,luis,0.5).	

	/* Opuestos*/
	contacto(juan,pepe,0.3).
	contacto(manolo,juan,0.6).
	contacto(luis,manolo,4.0).
	contacto(lucia,josemari,4.0).
	contacto(josemari,raul,3.0).
	contacto(felipe,luis,2.0).
	contacto(felipe,manolo,2.5).
	contacto(vidal,pepe,1.0).
	contacto(luis,pepe,0.5).	
	
	
 	miembro(V, [V|_]).
 	miembro(V, [_|L]):-
 		miembro(V,L).

	pinta([]).
 	pinta([H|T]):-
 		pinta(T),
 		write(H, '\n').
 		
 	/* Votante V1 convence a votante V2 si...*/
	convence(v(N1,CI1),v(N2,CI2)):-
		CI1>0.09, 				/* V1 tiene una cargaIdeologica significativa*/
		contacto(N1,N2,K), 			/* Contacto enre V1 y V2 de factorK */
		CI2 = K*CI1,
		CI2>0.09.
		/*CI2=CargaIdeologicaAConvencer.*/		/* Modifica carga ideologica*/
 		
 		
 	rutaIdeologica(A,A,ListaInicial,_,_,_):-
 		pinta(ListaInicial).
 		
 	rutaIdeologica(A,B,ListaInicial,_,LimActual,LimiteFinal):-
 		convence(A,C),
 		not(miembro(C, ListaInicial)),
 		ListaConversion = [C|ListaInicial],
 		NuevoLimite = LimActual + 1,
 		NuevoLimite <= LimiteFinal,
 		rutaIdeologica(C,B,ListaConversion, ListaConversion,NuevoLimite, LimiteFinal).

	practica():-
		rutaIdeologica(v(vidal,0.5), v(luis,CVL), [v(vidal,0.5)], ListaConversion,1,3),
		pinta(ListaConversion).
goal

	practica().
