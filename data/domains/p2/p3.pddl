(define (problem aimpaH) 
    
    (:domain lukasiewiczP2)
    (:objects 
        a b aa u1 u2 u3 u4 u5 u6 - formula
    )

    (:init
        (def a)
        (def b)
        (def aa)
        (implies aa a a) ; A -> A is our goal formula 
        (undef u1)
        (undef u2)
        (undef u3)
        (undef u4)
        (undef u5)
        (undef u6)
    )

    (:goal (provable aa))
)
