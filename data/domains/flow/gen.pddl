(define (domain flow_free)

(:requirements :strips :typing)

(:types
    color
    location
)

(:predicates
    (colored ?l - location ?c - color)
    (adjacent ?l1 - location ?l2 - location)
    (startpoint ?l - location ?c - color)
    (endpoint ?l - location ?c - color)
    (connected ?c - color)
)

(:action start
    :parameters (?l - location ?c - color)
    :precondition (startpoint ?l ?c)
    :effect (colored ?l ?c)
)

(:action move
    :parameters (?l1 ?l2 - location ?c - color)
    :precondition (and (colored ?l1 ?c) (adjacent ?l1 ?l2))
    :effect (colored ?l2 ?c)
)

(:action finish
    :parameters (?l1 ?l2 - location ?c - color)
    :precondition (and (colored ?l1 ?c) (adjacent ?l1 ?l2) (endpoint ?l2 ?c))
    :effect (connected ?c)
)

)