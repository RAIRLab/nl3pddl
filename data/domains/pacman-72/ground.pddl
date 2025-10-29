(define (domain pacman-72)
  (:requirements :strips :typing)
  (:types position)

  (:predicates
    (at ?pos - position)
    (not_at ?pos - position)          ; the complement of at
    (visited ?pos - position)
    (connected ?from ?to - position)
    (hasFood ?pos - position)
    (noFood ?pos - position)          ; the complement of hasFood
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
      (not (at ?from))        ; DELETE: Pacman is no longer at ?from
      (not_at ?from)
      (visited ?to)
      (not (not_at ?to))      ; DELETE: ?to is no longer marked as not_at 
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
      (not (hasFood ?pos))   ; DELETE: the food is gone
    )
  )
)