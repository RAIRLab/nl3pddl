(define (domain sliding-puzzle)
  (:requirements :strips :typing)
  
  (:types tile position)
  
  (:predicates
    (at ?t - tile ?p - position)
    (empty ?p - position)
    (adjacent ?p1 - position ?p2 - position)
  )

  (:action move
    :parameters (?t - tile ?from - position ?to - position)
    :precondition (and
      (at ?t ?from)
      (empty ?to)
      (adjacent ?from ?to)
    )
    :effect (and
      (not (at ?t ?from))
      (at ?t ?to)
      (not (empty ?to))
      (empty ?from)
    )
  )
)