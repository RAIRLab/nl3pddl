;Honkai Star Rail Pathfinder Domain

(define (domain pathfinder)

    ;remove requirements that are not needed
    (:requirements :strips :typing)

    (:types location direction - object)

    (:predicates
        (plate-at ?l - location)
        (wall-at ?l - location)
        (clear ?l - location)
        (connected ?l1 ?l2 - location ?d - direction) ;l1 is connected to l2 in direction
        (in-motion ?d - direction)
        (not-in-motion)
        (at ?l - location)          ;player here
    )

    (:action motion-clear
        :parameters (?l1 ?l2 - location ?d - direction)
        :precondition (and (in-motion ?d) (clear ?l2) (at ?l1) (connected ?l1 ?l2 ?d))
        :effect (and (at ?l2) (not (at ?l1)))
    )

    (:action motion-start
        :parameters (?d - direction)
        :precondition (not-in-motion)
        :effect (and (in-motion ?d) (not (not-in-motion)))
    )

    ; pass over a pressure plate
    ; put a wall at the location of the player so they can not come back that way
    (:action motion-plate
        :parameters (?l1 ?l2 - location ?d - direction)
        :precondition (and (at ?l1) (connected ?l1 ?l2 ?d) (plate-at ?l2) (in-motion ?d))
        :effect (and (at ?l2) (not (at ?l1)) (not (plate-at ?l2)) (wall-at ?l2))
    )

    ;knock into a wall
    (:action motion-wall
        :parameters (?l1 ?l2 - location ?d - direction)
        :precondition (and (at ?l1) (connected ?l1 ?l2 ?d) (wall-at ?l2) (in-motion ?d))
        :effect (and (not (in-motion ?d)) (not-in-motion))
    )
)