(define (domain sudoku)
  (:requirements :strips :typing)

  (:types
    pos row col box number
  )

  (:predicates
    (empty ?p - pos)
    (filled ?p - pos)
    (has-number ?p - pos ?n - number)
    (posdata ?p ?r ?c ?b)
    (not-in-row ?n - number ?r - row)
    (not-in-col ?n - number ?c - col)
    (not-in-box ?n - number ?b - box)
  )

  (:action place-number
    :parameters (?p - pos ?r - row ?c - col ?b - box ?n - number)
    :precondition (and
      (empty ?p)
      (posdata ?p ?r ?c ?b)
      (not-in-row ?n ?r)
      (not-in-col ?n ?c)
      (not-in-box ?n ?b)
    )
    :effect (and
      (filled ?p)
      (has-number ?p ?n)
      (not (empty ?p))
      (not (not-in-row ?n ?r))
      (not (not-in-col ?n ?c))
      (not (not-in-box ?n ?b))
    )
  )
)