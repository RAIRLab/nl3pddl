(define (domain hiking)
  (:requirements :strips :typing)
  (:types
    loc
  )

  (:predicates
    (at ?loc - loc)
    ;;(isWater ?loc - loc)
    (isDry ?loc - loc) ; Opposite of isWater
    (isHill ?loc - loc)
    (isFlat ?loc - loc) ; Opposite of isHill
    ;;(isGoal ?loc - loc)
    (adjacent ?loc1 - loc ?loc2 - loc)
  )

  (:action walk
    :parameters (?from - loc ?to - loc)
    :precondition (and
      (isFlat ?to)
      (at ?from)
      (adjacent ?from ?to)
      (isDry ?from))
    :effect (and
      (at ?to)
      (not (at ?from)))
  )

  (:action climb
    :parameters (?from - loc ?to - loc)
    :precondition (and
      (isHill ?to)
      (at ?from)
      (adjacent ?from ?to)
      (isDry ?from))
    :effect (and
      (at ?to)
      (not (at ?from)))
  )

)