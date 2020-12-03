/*****************************************************************************

		Copyright (c) My Company

 Project:  BALDES
 FileName: BALDES.PRO
 Purpose: No description
 Written by: Visual Prolog
 Comments:
******************************************************************************/

include "baldes.inc"

domains
	balde = integer
	limite = integer
	estado = e(balde,balde)
	lista = estado*
	
predicates
	escribe(lista)
	miembro(estado,lista)
	backtrack(estado,estado,lista,limite,limite)
	mover(estado,estado)
	baldes()
	
	

clauses
	/* REGLAS DE PRODUCION */
	
	/* llenar primer balde */
	mover(e(Xi,Y),e(Xf,Y)):-
		Xi<6,
		Xf=6.
	
	/* llenar segundo balde */
	mover(e(X,Yi),e(X,Yf)):-
		Yi<8,
		Yf=8.
	
	/* vaciar primer balde */
	mover(e(Xi,Y),e(Xf,Y)):-
		Xi>0,
		Xf=0.
		
	/* vaciar segundo balde */
	mover(e(X,Yi),e(X,Yf)):-
		Yi>0,
		Yf=0.
		
	/* descargar primero en segundo */
	mover(e(Xi,Yi),e(Xf,Yf)):-
		Xi>0, 8>=(Xi+Yi),
		Xf=0, Yf=(Xi+Yi).
		
	/* descargar segundo en primero */
	mover(e(Xi,Yi),e(Xf,Yf)):-
		Yi>0, 6>=(Xi+Yi),
		Yf=0, Xf=(Xi+Yi).
		
	/* llenar primero con segundo */
	mover(e(Xi,Yi),e(Xf,Yf)):-
		Yi>0,	Xi<6,
		Xf=6,	Yf=Yi-(6-Xi).
		
	/* llenar segundo con primero */
	mover(e(Xi,Yi),e(Xf,Yf)):-
		Xi>0,	Yi<8,
		Yf=8,	Xf=Xi-(8-Yi).
	
	
	/* COMUN */
	miembro(E, [E|_]).
	miembro(E, [_|L]):-
		miembro(E,L).
		
	escribe([]).
	escribe([H|T]):-
		escribe(T),
		write(H, '\n').
		
		
	backtrack(A,A,Lista,_,_):-
		escribe(Lista).
		
	backtrack(A,B,Lista,LimActual, Limite):-
		mover(A,C),
		not(miembro(C, Lista)),
		NuevoLimite = LimActual + 1,
		NuevoLimite <= Limite,
		backtrack(C,B,[C|Lista], NuevoLimite, Limite).
		
		
	baldes():-
		backtrack(e(0,0),e(_,4),[e(0,0)],0,6). 

goal

  baldes().
