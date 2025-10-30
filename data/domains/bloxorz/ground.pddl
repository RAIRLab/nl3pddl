(define (domain bloxorz)
  (:requirements :strips :typing)
  (:types tile block direction)
  (:constants north east west south - direction)

  (:predicates
    (standing-on ?b - block ?t - tile) ; block stands upright on one tile
    (lying-on ?b - block ?t - tile) ; block lies flat on a tile (one of the two)
    (adjacent ?t1 - tile ?t2 - tile ?d - direction)
    (target-tile ?t - tile)
    (perpendicular ?d1 ?d2)
  )

  (:action lay-down
    :parameters (?b - block ?from - tile ?to1 - tile ?to2 - tile ?d - direction)
    :precondition (and
      (standing-on ?b ?from)
      (adjacent ?to1 ?from ?d)
      (adjacent ?to2 ?to1 ?d)
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
      (adjacent ?t2 ?t1 ?d)
      (adjacent ?t3 ?t2 ?d)
    )
    :effect (and
      (not (laying-on ?b ?t1))
      (not (laying-on ?b ?t2))
      (standing-on ?b ?t3)
    )
  )

  (:action roll
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?t4 - tile ?blockd - direction ?tod - direction)
    :precondition (and
      (perpendicular ?blockd ?tod)
      (lying-on ?b ?t1)
      (lying-on ?b ?t2)
      (adjacent ?t2 ?t1 ?blockd)
      (adjacent ?t4 ?t3 ?blockd)
      (adjacent ?t3 ?t1 ?tod)
      (adjacent ?t4 ?t2 ?tod)
    )
    :effect (and
      (not (lying-on ?b ?t1))
      (not (lying-on ?b ?t2))    
      (lying-on ?b ?t3)
      (lying-on ?b ?t4)
    )
  )
)