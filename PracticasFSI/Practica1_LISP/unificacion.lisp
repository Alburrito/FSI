; Practica LISP - Fundamentos de Sistemas Inteligentes
; Álvaro Martín López - 70960937A - almarlop1998@usal.es
; 2020


; variable o constante
(defun atomo(var)
    (cond
        ((atom var) T)
        ((eq (first var) '?) T)
        (T NIL)
    )
)


; lista no vacia y no una variable
(defun lista(var)
    (if (and (listp var) (not (atomo var)))
        T
        NIL
    )
)


; lista de dos elementos siendo el primero una ? y el segundo un literal
; si var es atomo pero es lista, es porque es de la forma (? x)
(defun es_variable (var)
    (if (and (listp var) (atomo var))
        T
        NIL
    )
)


;busca var en list recursivamente.
(defun aparece (var list)
    (when (lista list)
        (setf encontrado NIL) ; flag para saber si lo encontramos
        (loop for elemento in list do ; iteramos sobre sus elementos
            (prog ()
                (if (atomo elemento) ;si el elemento es atomico, comparamos
                    (when (equal elemento var) ;si coincide con var, APARECE
                        (return-from aparece T)
                    )
                    (setf encontrado (aparece var elemento)) ; si no es atomo, es lista. Buscamos var en la nueva lista y guardamos lo devuelto en encontrado
                )
                (when (equal encontrado T) ; si ya lo ha encontrado no hace falta que busque mas
                    (return-from aparece T)
                )
            )
        )
    )
    (return-from aparece NIL) ; no se ha encontrado o habria salido antes O list no es una lista
)

;se busca la variable en la lista de sustituciones
;se asume que var es variable y lista una lista de tuplas (SUSTITUCION variable)
(defun buscar_sustitucion (var l_sust)
    (loop for sustitucion in l_sust do ;
        (when (equal var (second sustitucion)) ;si coinciden las variables a sustituir
            (return-from buscar_sustitucion (first sustitucion)) ; se devuelve la sustitucion correspondiente
        )
    )
    (return-from buscar_sustitucion var) ; si no se ha encontrado se devuelve la variable original
)



;recorre los elementos de s2 creando la lista resultante de aplicar las reglas de s1
;se asume que s1 es una lista cuyos elementos son tuplas (SUSTITUCION variable)
(defun aplicar (s1 s2)
    (prog (result_list)
        (setf result_list '())
        (if (lista s2)
            (loop for element in s2 do
                (if (atomo element)
                    (if (es_variable element)
                        (setf element_to_append (buscar_sustitucion element s1)) ;se añadirá la variable o la sustitución si la hubiese
                        (setf element_to_append element) ; se añadirá una constante
                    )
                    (setf element_to_append (aplicar s1 element)) ;es una lista, asi que se añadira el resultado de aplicar las reglas a dicha lista
                )
                (setf result_list (append result_list (list element_to_append)))
            )
            (prog()
                (if (es_variable s2) ;si no es lista, es un atomo
                    (setf element_to_append (buscar_sustitucion s2 s1)) ;se añadirá la variable o la sustitución si la hubiese
                    (setf element_to_append s2) ; se añadirá una constante
                )
                (setf result_list (append result_list element_to_append))
            )
        )
        (return-from aplicar result_list)
   )
)


;aplicar reglas de c2 a los numeradores de las reglas de c1 y crear una lista con los resultados
;añadir a la lista las reglas de c2 cuyos denominadores no coincidan con ninguno de la nueva lista
;devolver la lista
;se asume que c1 y c2 son listas de reglas
(defun componer (c1 c2)
    (setf c1c2 '())
    (loop for rule1 in c1 do
        (setf num (first rule1))
        (setf den (second rule1))
        (setf new_rule (list (aplicar c2 num) den))
        (setf c1c2 (append c1c2 (list new_rule)))
    )
    (loop for rule2 in c2 do
        (setf den (second rule2))
        (setf encontrado NIL)
        (loop for rule in c1c2 do
            (when (equal den (second rule))
                (setf encontrado T)
            )
        )
        (unless (equal encontrado T)
             (setf c1c2 (append c1c2 (list rule2)))
        )
    )
    (return-from componer c1c2)
)


;unificar
(defun unificar (e1 e2)
    (when (and (lista e1) (= 1 (length e1)))
        (setf e1 (first e1))
    )
    (when (and (lista e2) (= 1 (length e2)))
        (setf e2 (first e2))
    )

    ;primer bloque de unificar (lineas 1-10)
    (when (and (not (atomo e1)) (atomo e2))
        (setf tmp e1)
        (setf e1 e2)
        (setf e2 tmp)
    )
    (when (atomo e1)
        (when (equal e1 e2)
            (return-from unificar '())
        )
        (when (es_variable e1)
            (if (aparece e1 e2)
                (return-from unificar 'FALLO)
                (return-from unificar (list (list e2 e1)))
            )
        )
        (when (es_variable e2)
            (return-from unificar (list (list e1 e2)))
        )
        (return-from unificar 'FALLO)
     )
     ;si ninguno es atomo, segundo bloque de unificar (lineas 12-20)
     (prog (F1 F2 T1 T2 G1 G2 Z1 Z2)
         (setf F1 (first e1))
         (setf T1 (rest e1))
         (setf F2 (first e2))
         (setf T2 (rest e2))
         (setf Z1 (unificar F1 F2))
         (when (equal Z1 'FALLO)
             (return-from unificar 'FALLO)
         )
         (setf G1 (aplicar Z1 T1))
         (setf G2 (aplicar Z1 T2))
         (setf Z2 (unificar G1 G2))
         (when (equal Z2 'FALLO)
             (return-from unificar 'FALLO)
         )
         (return-from unificar (componer Z1 Z2))
     )
)







; PRUEBAS
(defun test_unificar (e1 e2)
    (write-line "---------------------------------------------------")
    (write "e1: ")(write e1)(write-line "")
    (write "e2: ")(write e2)(write-line "")

    (setf reglas_unificacion (unificar e1 e2))
    (if (equal reglas_unificacion 'FALLO)
        (write-line "RESULTADO: FALLO")
        (prog (e1_unficado e2_unficado)
            (write "Reglas_resultado: ")(write reglas_unificacion)(write-line "")
            (setf e1_unificado (aplicar reglas_unificacion e1))
            (setf e2_unificado (aplicar reglas_unificacion e2))
            (write "e1_unificado: ")(write e1_unificado)(write-line "")
            (write "e2_unificado: ")(write e2_unificado)(write-line "")
            (if (equal e1_unificado e2_unificado)
                (write-line "EXITO AL UNIFICAR")
                (write-line "FRACASO AL UNIFICAR")
            )
        )
    )
    (write-line "---------------------------------------------------")
)



(write-line "")
(write-line "+-------------------------------------------------+")
(write-line "|--------------- PRUEBA UNIFICACION --------------|")
(write-line "+-------------------------------------------------+")
(write-line "Alvaro Martin Lopez - 70960937A - 2020")
(write-line "almarlop1998@usal.es")
(write-line "")

(setf u1 '(P (? X) (F (? X)))) ; P(x, F(x))
(setf u2 '(P A (? Y))) ; P(A,y)

(setf u3 '(P (? X) (F (? X)))); P(x, F(x))
(setf u4 '(P A B)); P(A,B)

;unificacion jesus
;f           f
(setf j1 'f)
(setf j2 'f)

;f(x)        f(A)
(setf j3 '(f (? x)))
(setf j4 '(f A))

;f(x,y)      f(A,B)
(setf j5 '(f (? x) (? y)))
(setf j6 '(f A B))

;f(x, g(x))  f(a, g(a))
(setf j7 '(f (? x) (g (? x))))
(setf j8 '(f a (g a)))

;F(y,x)      f(x,a)
(setf j9 '(f (? y) (? x)))
(setf j10 '(f (? x) a))


(test_unificar u1 u2)(write-line "")
(test_unificar u3 u4)(write-line "")
(test_unificar j1 j2)(write-line "")
(test_unificar j3 j4)(write-line "")
(test_unificar j5 j6)(write-line "")
(test_unificar j7 j8)(write-line "")
(test_unificar j9 j10)
