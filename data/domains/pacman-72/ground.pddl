(define (domain pacman)
  (:requirements :strips :typing)
  (:types position)

  (:predicates
    (at ?pos - position)
    (not_at ?pos - position)          ; complement of at
    (visited ?pos - position)
    (connected ?from ?to - position)
    (eat ?pos - position)
    (hasFood ?pos - position)
    (noFood ?pos - position)          ; complement of hasFood
    (carryingFood)
  )

  (:action move
    :parameters (?from ?to - position)
    :precondition (and
      (at ?from)
      (not_at ?to)
      (connected ?from ?to)
    )
    :effect (and
      (at ?to)
      (not_at ?from)
      (visited ?to)
    )
  )

  (:action eat
    :parameters (?pos - position)
    :precondition (and
      (at ?pos)
      (hasFood ?pos)
    )
    :effect (and
      (carryingFood)
      (noFood ?pos)
    )
  )
)