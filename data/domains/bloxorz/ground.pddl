(define (domain bloxorz)
  (:requirements :strips :typing)
  (:types tile block)

  (:predicates
    (on ?b - block ?t - tile) ; block stands upright on one tile
    (occupies ?b - block ?t1 - tile ?t2 - tile) ; block lies flat on two tiles
    (adjacent-north ?t1 - tile ?t2 - tile)
    (adjacent-south ?t1 - tile ?t2 - tile)
    (adjacent-east ?t1 - tile ?t2 - tile)
    (adjacent-west ?t1 - tile ?t2 - tile)
    (goal-tile ?t - tile)
  )

  ;; ===== Standing --> Lying-Y =====
  (:action move-north-from-standing
    :parameters (?b - block ?from - tile ?to - tile)
    :precondition (and
      (on ?b ?from)
      (adjacent-north ?to ?from)
    )
    :effect (and
      (not (on ?b ?from))
      (occupies ?b ?from ?to)
    )
  )

  (:action move-south-from-standing
    :parameters (?b - block ?from - tile ?to - tile)
    :precondition (and
      (on ?b ?from)
      (adjacent-south ?to ?from)
    )
    :effect (and
      (not (on ?b ?from))
      (occupies ?b ?to ?from)
    )
  )

  ;; ===== Standing --> Lying-X =====
  (:action move-east-from-standing
    :parameters (?b - block ?from - tile ?to - tile)
    :precondition (and
      (on ?b ?from)
      (adjacent-east ?to ?from)
    )
    :effect (and
      (not (on ?b ?from))
      (occupies ?b ?from ?to)
    )
  )

  (:action move-west-from-standing
    :parameters (?b - block ?from - tile ?to - tile)
    :precondition (and
      (on ?b ?from)
      (adjacent-west ?to ?from)
    )
    :effect (and
      (not (on ?b ?from))
      (occupies ?b ?to ?from)
    )
  )

  ;; ===== Lying-Y --> Standing =====
  (:action move-north-from-lying-y
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-north ?t2 ?t1)
      (adjacent-north ?t3 ?t2)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (on ?b ?t3)
    )
  )

  (:action move-south-from-lying-y
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-south ?t1 ?t2)
      (adjacent-south ?t3 ?t1)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (on ?b ?t3)
    )
  )

  ;; ===== Lying-X --> Standing =====
  (:action move-east-from-lying-x
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-east ?t2 ?t1)
      (adjacent-east ?t3 ?t2)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (on ?b ?t3)
    )
  )

  (:action move-west-from-lying-x
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-west ?t1 ?t2)
      (adjacent-west ?t3 ?t1)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (on ?b ?t3)
    )
  )

  ;; ===== Lying-Y --> Lying-Y ===== (rolling without standing)
  (:action move-north-while-lying-y
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?t4 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-north ?t2 ?t1)
      (adjacent-north ?t3 ?t2)
      (adjacent-north ?t4 ?t3)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (occupies ?b ?t3 ?t4)
    )
  )

  (:action move-south-while-lying-y
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?t4 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-south ?t1 ?t2)
      (adjacent-south ?t3 ?t1)
      (adjacent-south ?t4 ?t3)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (occupies ?b ?t3 ?t4)
    )
  )

  ;; ===== Lying-X --> Lying-X =====
  (:action move-east-while-lying-x
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?t4 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-east ?t2 ?t1)
      (adjacent-east ?t3 ?t2)
      (adjacent-east ?t4 ?t3)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (occupies ?b ?t3 ?t4)
    )
  )

  (:action move-west-while-lying-x
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?t4 - tile)
    :precondition (and
      (occupies ?b ?t1 ?t2)
      (adjacent-west ?t1 ?t2)
      (adjacent-west ?t3 ?t1)
      (adjacent-west ?t4 ?t3)
    )
    :effect (and
      (not (occupies ?b ?t1 ?t2))
      (occupies ?b ?t3 ?t4)
    )
  )
)