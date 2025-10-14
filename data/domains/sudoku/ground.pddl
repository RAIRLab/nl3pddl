(define (domain sudoku)
  (:requirements :strips :typing)

  (:types
    cell number
  )

  (:predicates
    (empty ?c - cell)
    (filled ?c - cell)
    (has-value ?c - cell ?n - number)
    (not-has-value ?c - cell ?n - number)
    (no-conflict ?c - cell ?n - number)
  )

  (:action assign
    :parameters (?c - cell ?n - number)
    :precondition (and
      (empty ?c)
      (not-has-value ?c ?n)
      (no-conflict ?c ?n)
    )
    :effect (and
      (filled ?c)
      (has-value ?c ?n)
      (not (empty ?c))          ; DELETE: cell is no longer empty
      (not (not-has-value ?c ?n)) ; DELETE: now it has the value
    )
  )
)