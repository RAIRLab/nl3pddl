(define (domain pathfinder)

(:requirements :strips :typing)

(:types location direction - object)

(:predicates
    (plate-at ?l - location)
    (wall-at ?l - location)
    (clear ?l - location)
    (connected ?l1 ?l2 - location ?d - direction)
    (in-motion ?d - direction)
    (not-in-motion)
    (at ?l - location)
)

(:action motion-clear
    :parameters (?l1 ?l2 - location ?d - direction)
    :precondition (and (in-motion ?d) (at ?l1) (connected ?l1 ?l2 ?d) (clear ?l2))
    :effect (and (not (at ?l1)) (at ?l2))
)

(:action motion-start
    :parameters (?d - direction)
    :precondition (not-in-motion)
    :effect (and (not (not-in-motion)) (in-motion ?d))
)

(:action motion-plate
    :parameters (?l1 ?l2 - location ?d - direction)
    :precondition (and (in-motion ?d) (at ?l1) (connected ?l1 ?l2 ?d) (plate-at ?l2))
    :effect (and (not (at ?l1)) (at ?l2) (not (plate-at ?l2)) (wall-at ?l2))  ;; Removed motion stopping effects
)

(:action motion-wall
    :parameters (?l1 ?l2 - location ?d - direction)
    :precondition (and (in-motion ?d) (at ?l1) (connected ?l1 ?l2 ?d) (wall-at ?l2))
    :effect (and (not (in-motion ?d)) (not-in-motion))
)

)