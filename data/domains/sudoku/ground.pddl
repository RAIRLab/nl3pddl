(define (domain sudoku)
  (:requirements :strips :typing)

  (:types
    pos row col box number
  )

  (:predicates
    (empty ?p - pos)
    (filled ?p - pos)
    (posdata ?p ?r ?c ?b)
  )

  (:action place-number
    :parameters (?p - pos ?r - row ?c - col ?b - box ?n - number)
    :precondition (and
      (empty ?c)
      (posdata ?p ?r ?c ?b)
      (not-in-row ?n ?r)
      (not-in-col ?n ?c)
      (not-in-box ?n ?b)
    )
    :effect (and
      (filled ?p)
      (not (empty ?p))
      (not (not-in-row ?n ?r))
      (not (not-in-col ?n ?c))
      (not (not-in-box ?n ?b))
    )
  )
)