(define (domain pacman_ai)
  (:requirements :strips :typing)
  (:types node)

  (:predicates
    (has_food ?location - node)
    (no_food ?location - node)          ; complement of has_food
    (is_opponent_ghost ?location - node)
    (safe_from_ghost ?location - node)  ; complement of is_opponent_ghost
    (at ?location - node)
    (not_at ?location - node)           ; complement of at
    (is_visited ?location - node)
    (connected ?n1 ?n2 - node)
  )

  (:action move_pacman
    :parameters (?start ?end - node)
    :precondition (and
      (at ?start)
      (no_food ?end)
      (safe_from_ghost ?end)
      (connected ?start ?end)
    )
    :effect (and
      (not_at ?start)
      (at ?end)
      (is_visited ?end)
      (no_food ?start)                 ; keep complements consistent
    )
  )

  (:action eat_food
    :parameters (?start ?end - node)
    :precondition (and
      (at ?start)
      (has_food ?end)
      (safe_from_ghost ?end)
      (connected ?start ?end)
    )
    :effect (and
      (at ?end)
      (not_at ?start)
      (is_visited ?end)
      (no_food ?end)                    ; marking food consumed
    )
  )
)