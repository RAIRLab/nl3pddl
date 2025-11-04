(define (domain hiking)
  (:requirements :strips :typing)
  (:types loc)
  (:predicates
    (adjacent ?loc1 - loc ?loc2 - loc)
    (iswater ?loc - loc)
    (at ?loc - loc)
    (isgoal ?loc - loc)
    (ontrail ?from - loc ?to - loc)
    (ishill ?loc - loc)
    (trailstart ?loc - loc)
    (walking)
    (climbing)
  )

  (:action walk
    :parameters (?from - loc ?to - loc)
    :precondition (and
      (at ?from)
      (adjacent ?from ?to)
      (ontrail ?from ?to)
      (not (iswater ?to))
    )
    :effect (and
      (not (at ?from))
      (at ?to)
    )
  )

  (:action climb
    :parameters (?l - loc)
    :precondition (and
      (at ?l)
      (ishill ?l)
      (walking)
    )
    :effect (and
      (climbing)
      (not (walking))
    )
  )
)