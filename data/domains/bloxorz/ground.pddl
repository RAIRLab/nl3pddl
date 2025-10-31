(define (domain bloxorz)
  (:requirements :strips :typing)
  (:types tile block direction)
  (:constants north east west south - direction)

  (:predicates
    (standing-on ?b - block ?t - tile) ; block stands upright on one tile
    (lying-on ?b - block ?t - tile) ; block lies flat on a tile (one of the two)
    (adjacent ?t1 - tile ?t2 - tile ?d - direction)  ; direction of t2 from t1
    (perpendicular ?d1 ?d2)
  )

  (:action lay-down
    :parameters (?b - block ?from - tile ?to1 - tile ?to2 - tile ?d - direction)
    :precondition (and
      (standing-on ?b ?from)
      (adjacent ?from ?to1 ?d)
      (adjacent ?to1 ?to2 ?d)
    )
    :effect (and
      (not (standing-on ?b ?from))
      (lying-on ?b ?to2)
      (lying-on ?b ?to1)
    )
  )

  (:action stand-up
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?d - direction)
    :precondition (and
      (lying-on ?b ?t1)
      (lying-on ?b ?t2)
      (adjacent ?t1 ?t2 ?d)
      (adjacent ?t2 ?t3 ?d)
    )
    :effect (and
      (not (lying-on ?b ?t1))
      (not (lying-on ?b ?t2))
      (standing-on ?b ?t3)
    )
  )

  (:action roll
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?t4 - tile ?blockd - direction ?tod - direction)
    :precondition (and
      (perpendicular ?blockd ?tod)
      (lying-on ?b ?t1)
      (lying-on ?b ?t2)
      (adjacent ?t1 ?t2 ?blockd)
      (adjacent ?t3 ?t4 ?blockd)
      (adjacent ?t1 ?t3 ?tod)
      (adjacent ?t2 ?t4 ?tod)
    )
    :effect (and
      (not (lying-on ?b ?t1))
      (not (lying-on ?b ?t2))    
      (lying-on ?b ?t3)
      (lying-on ?b ?t4)
    )
  )
)