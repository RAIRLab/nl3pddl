

(define (domain flow)

    (:requirements :strips :typing)

    (:types
        color
        location
    )

    (:predicates
        ;The finger is off the board, we can begin any flow
        (offboard)
        ; the location has no color
        (empty ?l - location)
        ; negation of empty predicate
        (not-empty ?l - location)
        ; the location l has color c
        (color-at ?l - location ?c - color )
        ; l1 is an adjacent location to l2
        (adjacent ?l1 - location ?l2 - location)
        ; l is the end point for the flow of color c
        (flow-end ?l - location ?c - color)
        ; the player is at l1 drawing a flow of color c
        (flow-at ?l1 - location ?c - color)
        ; the flow for color c is completed
        (flow-complete ?c - color)
    )

    ;start the flow of color c
    (:action start
        :parameters (?l - location ?c - color)
        :precondition (and (offboard) (empty ?l) (flow-end ?l ?c)) 
        :effect (and (not (offboard)) (not (empty ?l)) (not-empty ?l) (flow-at ?l ?c) (color-at ?l ?c))
    )

    (:action move
        :parameters (?l1  ?l2 - location ?c - color)
        :precondition (and (flow-at ?l1 ?c) (empty ?l2) (adjacent ?l1 ?l2)) 
        :effect (and (not (flow-at ?l1 ?c)) (not (empty ?l2)) (flow-at ?l2 ?c) (not-empty ?l2) (color-at ?l2 ?c))
    )

    ;end the flow of color c
    (:action finish
        :parameters (?l1  ?l2 - location ?c - color)
        :precondition (and (flow-at ?l1 ?c) (empty ?l2) (flow-end ?l2 ?c) (adjacent ?l1 ?l2)) 
        :effect (and (not (flow-at ?l1 ?c)) (not (empty ?l2)) (not-empty ?l2) (offboard) (color-at ?l2 ?c) (flow-complete ?c))
    )
)