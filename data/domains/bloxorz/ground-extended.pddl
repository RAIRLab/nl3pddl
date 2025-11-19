(define (domain bloxorz)
  (:requirements :strips :typing)
  (:types tile block direction)
  (:constants north east west south - direction)

  (:predicates
    (standing-on ?b - block ?t - tile) ; block stands upright on one tile
    (lying-on ?b - block ?t - tile) ; block lies flat on a tile (one of the two)
    (adjacent ?t1 - tile ?t2 - tile ?d - direction)  ; direction of t2 from t1
    (perpendicular ?d1 - direction ?d2 - direction)
    (active ?t - tile)
    (hard ?t - tile)
    (activating ?t - tile ?t2 - tile)
  )

  (:action lay-down
    :parameters (?b - block ?from - tile ?to1 - tile ?to2 - tile ?d - direction)
    :precondition (and
      (active ?to1)
      (active ?to2)
      (standing-on ?b ?from)
      (adjacent ?from ?to1 ?d)
      (adjacent ?to1 ?to2 ?d)
    )
    :effect (and
      (not (standing-on ?b ?from))
      (lying-on ?b ?to2)
      (lying-on ?b ?to1)

      (forall (?x - tile)
        (when (and (activating ?to1 ?x) (not (active ?x)) (not (hard ?to1)))
          (active ?x)))
      (forall (?x - tile)
        (when (and (activating ?to2 ?x) (not (active ?x)) (not (hard ?to2)))
          (active ?x)))

      (forall (?x - tile)
        (when (and (activating ?to1 ?x) (active ?x) (not (hard ?to1)))
          (not (active ?x))))
      (forall (?x - tile)
        (when (and (activating ?to2 ?x) (active ?x) (not (hard ?to2)))
          (not (active ?x))))
    )
  )

  (:action stand-up
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?d - direction)
    :precondition (and
      (active ?t3)
      (lying-on ?b ?t1)
      (lying-on ?b ?t2)
      (adjacent ?t1 ?t2 ?d)
      (adjacent ?t2 ?t3 ?d)
    )
    :effect (and
      (not (lying-on ?b ?t1))
      (not (lying-on ?b ?t2))
      (standing-on ?b ?t3)
      (forall (?x - tile)
        (when (and (activating ?t3 ?x) (not (active ?x)))
          (active ?x)))
      (forall (?x - tile)
        (when (and (activating ?t3 ?x) (active ?x))
          (not (active ?x))))

    )
  )

  (:action roll
    :parameters (?b - block ?t1 - tile ?t2 - tile ?t3 - tile ?t4 - tile ?blockd - direction ?tod - direction)
    :precondition (and
      (perpendicular ?blockd ?tod)
      (active ?t3)
      (active ?t4)
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
 
       (forall (?x - tile)
        (when (and (activating ?t3 ?x) (not (active ?x)) (not (hard ?t3)))
          (active ?x)))
      (forall (?x - tile)
        (when (and (activating ?t4 ?x) (not (active ?x)) (not (hard ?t4)))
          (active ?x)))

      (forall (?x - tile)
        (when (and (activating ?t3 ?x) (active ?x) (not (hard ?t3)))
          (not (active ?x))))
      (forall (?x - tile)
        (when (and (activating ?t4 ?x) (active ?x) (not (hard ?t4)))
          (not (active ?x))))
 
    )
  )
)