(define (problem p1) (:domain pathfinder)
(:objects 
    n e s w - direction
    l1 l2 l3 l4 
    l5 l6 l7 l8 lw 
    l9 l10 l11 l12 - location
)

(:init
    (connected l1 l2 e)
    (connected l2 l1 w)
    (connected l2 l3 e)
    (connected l3 l2 w)
    (connected l3 l4 e)
    (connected l4 l3 w)
    
    (connected l5 l6 e)
    (connected l6 l5 w)
    (connected l6 l7 e)
    (connected l7 l6 w)
    (connected l7 l8 e)
    (connected l8 l7 w)

    (connected l9 l10 e)
    (connected l10 l9 w)
    (connected l10 l11 e)
    (connected l11 l10 w)
    (connected l11 l12 e)
    (connected l12 l11 w)
    (connected l8 lw e)
    (connected lw l8 w)

    (connected l1 l5 s)
    (connected l5 l1 n)
    (connected l2 l6 s)
    (connected l6 l2 n)
    (connected l3 l7 s)
    (connected l7 l3 n)
    (connected l4 l8 s)
    (connected l8 l4 n)

    (connected l5 l9 s)
    (connected l9 l5 n)
    (connected l6 l10 s)
    (connected l10 l6 n)
    (connected l7 l11 s)
    (connected l11 l7 n)
    (connected l8 l12 s)
    (connected l12 l8 n)
    
    (wall-at lw)
    (wall-at l1)
    (clear l2)
    (clear l3)
    (clear l4)
    (clear l5)
    (plate-at l6)
    (clear l7)
    (clear l8)
    (clear l9)
    (clear l10)
    (clear l11)
    (clear l12)

    (at l9)
    (not-in-motion)

)

(:goal (and
    (at l3)
))
)
