(define (domain flow_free)

    (:requirements :strips :typing)

    (:types
        color
        location
    )

    (:predicates
        (offboard)
        (empty ?l - location)
        (not-empty ?l - location)
        (color-at ?l - location ?c - color)
        (adjacent ?l1 - location ?l2 - location)
        (flow-end ?l - location ?c - color)
        (flow-at ?l1 - location ?c - color)
        (flow-complete ?c - color)
        (start ?l - location ?c - color)
        (move ?l1 - location ?l2 - location ?c - color)
        (finish ?l1 - location ?l2 - location ?c - color)
    )

    (:action start
        :parameters (?l - location ?c - color)
        :precondition (and (flow-end ?l ?c) (not (flow-complete ?c)))
        :effect (start ?l ?c)
    )

    (:action move
        :parameters (?l1 ?l2 - location ?c - color)
        :precondition (and (not (offboard)) (adjacent ?l1 ?l2) (empty ?l2) (start ?l1 ?c) (not (finish ?l1 ?l2 ?c)))
        :effect (and (move ?l1 ?l2 ?c) (flow-at ?l2 ?c))
    )

    (:action finish
        :parameters (?l1 ?l2 - location ?c - color)
        :precondition (and (not (offboard)) (adjacent ?l1 ?l2) (color-at ?l1 ?c) (start ?l1 ?c) (move ?l1 ?l2 ?c) (flow-end ?l2 ?c))
        :effect (and (finish ?l1 ?l2 ?c) (flow-complete ?c))
    )
)