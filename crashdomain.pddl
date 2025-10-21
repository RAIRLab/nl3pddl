(define (domain flow)
  (:requirements :strips :typing)
  (:types color location)
  (:predicates
    (empty ?l - location)
    (color-at ?l - location ?c - color)
    (flow-end ?l - location ?c - color)
    (not-empty ?l - location)
    (flow-complete ?c - color)
    (adjacent ?l1 - location ?l2 - location)
    (offboard)
    (flow-at ?l - location ?c - color)
  )

  (:action start
    :parameters (?l - location ?c - color)
    :precondition (and
      (offboard)
      (flow-end ?l ?c)
      (color-at ?l ?c)
    )
    :effect (and
      (not (offboard))
      (flow-at ?l ?c)
    )
  )

  (:action move
    :parameters (?from - location ?to - location ?c - color)
    :precondition (and
      (flow-at ?from ?c)
      (adjacent ?from ?to)
      (empty ?to)
    )
    :effect (and
      (not (empty ?to))
      (not-empty ?to)
      (flow-at ?to ?c)
      (color-at ?to ?c)
    )
  )

  (:action finish
    :parameters (?from - location ?to - location ?c - color)
    :precondition (and
      (flow-at ?from ?c)
      (adjacent ?from ?to)
      (flow-end ?to ?c)
    )
    :effect (and
      (flow-at ?to ?c)
      (flow-complete ?c)
    )
  )
)