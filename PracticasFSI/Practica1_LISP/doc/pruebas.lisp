(defun test_unificar (e1 e2)
    (write-line "---------------------------------------------------"
    (write-line "Prueba Unificación)
    (write 'e1:)(write e1)(write-line "")
    (write 'e2:)(write e2)(write-line "")

    (setf reglas_unificacion (unificar e1 e2))
    (if (equal reglas_unificacion 'FALLO)
        (write-line "RESULTADO: FALLO")
        (prog (e1_unficado e2_unficado)
            (write 'Reglas_resultado:)(write reglas_unificacion)(write-line "")
            (setf e1_unficado (aplicar reglas_unificacion e1))
            (setf e2_unficado (aplicar reglas_unificacion e2))
            (write 'e1_unficado:)(write e1_unficado)(write-line "")
            (write 'e2_unficado:)(write e2_unficado)(write-line "")
            (if (equal e1_unificado e2_unificado)
                (write-line "EXITO AL UNIFICAR")
                (write-line "FRACASO AL UNIFICAR") 
            )
            (write-line "")
        )
    )
    (write-line "---------------------------------------------------"
)


(write-line "")
(write-line "------------- PRUEBA APLICACION -------------")
(setf a1 '((A (? x)) ((? y) (? z)) ((f (? h)) (? k))))
(setf a2 '(A (g (? k)) (f2 (? z))))

(write-line "A1:")
(write a1)(write-line "")
(write-line "A2:")
(write a2)(write-line "")

(write-line "")

(write-line "Aplicar a1 sobre a2. Esperado:")
(write-line "Resultado esperado:")
(write-line "(A (G (F (? H))) (F2 (? Y)))")
(write-line "Resultado obtenido: ")
(write (aplicar a1 a2))(write-line "")
(write-line "")




(write-line "")
(write-line "------------- PRUEBA COMPOSICION -------------")
(setf c1 '(((G (? X) (? Y)) (? Z))))
(setf c2 '((A (? X)) (B (? Y)) (C (? W)) (D (? Z))))

(write-line "C1:")
(write c1)(write-line "")
(write-line "C2:")
(write c2)(write-line "")

(write-line "")

(write-line "Componer C1C2")
(write-line "Resultado esperado:")
(write-line "(((G A B) (? Z)) (A (? X)) (B (? Y)) (C (? W)))")
(write-line "Resultado obtenido: ")
(write (componer c1 c2))(write-line "")
(write-line "")




(write-line "")
(write-line "------------- PRUEBA UNIFICACION -------------")
(setf u1 '(P (? X) (F (? X)))) ; P(x, F(x))
(setf u2 '(P A (? Y))) ; P(A,y)

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


(write-line "UNIFICAR U1 y U2")
(write-line "U1:")
(write u1)(write-line "")
(write-line "U2:")
(write u2)(write-line "")

(write-line "")

(write-line "Resultado esperado:")
(write-line "((A (? x)) ((F A) (? Y)))")
(write-line "Resultado obtenido: ")
(write (unificar u1 u2))(write-line "")
(write-line "")


