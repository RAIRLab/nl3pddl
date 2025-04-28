(define (domain gripperStrips)

    (:requirements :strips :typing )

    (:types room obj robot gripper)

    (:predicates 
        (at-robot ?r - room)
        (free ?g - gripper)
        (carry ?o - obj ?g - gripper)
        (at ?o - obj ?r - room)
    )

    (:action move
        :parameters (?from ?to - room)
        :precondition (and (at-robot ?from))
        :effect (and (at-robot ?to) (not (at-robot ?from)))
    )

    (:action pick
        :parameters (?o - obj ?r - room ?g - gripper)
        :precondition (and (at ?o ?r) (at-robot ?r) (free ?g))
        :effect (and (carry ?o ?g) (not (at ?o ?r)) (not (free ?g)))
    )

    (:action drop
        :parameters (?o - obj ?r - room ?g - gripper)
        :precondition (and (carry ?o ?g) (at-robot ?r))
        :effect (and (at ?o ?r) (free ?g) (not (carry ?o ?g)))
    )
)