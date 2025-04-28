(define (problem aimpa) 
    
    (:domain lukasiewiczP2)
    (:objects 
        a aa aaa - formula
    )
    (:init
        (def a)
        (def aa)
        (def aaa)
        (implies aa a a) 
        (def aaa)
        (implies aaa a aa)
    )

    (:goal (provable aaa))
)