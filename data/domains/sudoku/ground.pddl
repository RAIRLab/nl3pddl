(define (domain sudoku)
  (:requirements :adl :typing)

  (:types
      cell number
  )

  (:predicates
      ;; Cell state
      (empty ?c - cell)
      (has-value ?c - cell ?n - number)

      ;; Relations between cells
      (same-row ?c1 - cell ?c2 - cell)
      (same-col ?c1 - cell ?c2 - cell)
      (same-box ?c1 - cell ?c2 - cell)
  )

  ;; Action: assign a number to an empty cell if it's not conflicting
  (:action assign
    :parameters (?c - cell ?n - number)
    :precondition (and
        (empty ?c)
        ;; No conflict in same row
        (forall (?c2 - cell)
            (imply (same-row ?c ?c2)
                   (not (has-value ?c2 ?n))))
        ;; No conflict in same column
        (forall (?c3 - cell)
            (imply (same-col ?c ?c3)
                   (not (has-value ?c3 ?n))))
        ;; No conflict in same box
        (forall (?c4 - cell)
            (imply (same-box ?c ?c4)
                   (not (has-value ?c4 ?n))))
    )
    :effect (and
        (has-value ?c ?n)
        (not (empty ?c))
    )
  )
)