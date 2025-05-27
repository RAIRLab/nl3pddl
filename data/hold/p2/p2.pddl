(define (problem aimpa) 
    
    (:domain lukasiewiczP2)
    (:objects 
        a b aa ba baa aba abaa abaaa abaaabaaa - formula
    )

    (:init
        (def a)
        (def b)
        (def aa)
        (implies aa a a) ; A -> A is our goal formula 
        (def ba)
        (implies ba b a)
        (def baa)
        (implies baa ba a)
        (def aba)
        (implies aba a ba)
        (def abaa)
        (implies abaa a baa)
        (def abaaa)
        (implies abaaa aba aa)
        (def abaaabaaa)
        (implies abaaabaaa abaa abaaa)
    )

    (:goal (provable aa))
)
