(define (domain pacman)
    (:requirements :typing)
    (:types position)

    (:predicates
        (move ?from ?to - position)
        (at ?pos - position)
        (visited ?pos - position)
        (connected ?from ?to - position)
        (eat ?pos - position)
        (hasFood ?pos - position)
        (carryingFood)
    )

    (:action move
        :parameters
            (?from ?to - position)
        :precondition
            (and
                (at ?from)
                (connected ?from ?to)
            )
        :effect
            (and
                (at ?to)
                (not (at ?from))
                (visited ?to)
            )
    )

    (:action eat
        :parameters
            (?pos - position)
        :precondition
            (and
                (at ?pos)
                (hasFood ?pos)
            )
        :effect
            (and
                (carryingFood)
                (not (hasFood ?pos))
            )
    )
)