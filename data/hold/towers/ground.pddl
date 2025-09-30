
(define (domain hanoi)
  (:requirements :strips :typing)
  (:types peg disk)

  (:predicates
    (on ?d - disk ?l - location)     ; disk ?d is on location ?l (peg or disk)
    (clear ?l - location)            ; nothing on top of location ?l
    (smaller ?x - disk ?y - disk))   ; disk x is smaller than disk y

  ; Move a clear disk onto a clear peg
  (:action move-to-peg
    :parameters (?d - disk ?from - location ?to - peg)
    :precondition (and
      (on ?d ?from)
      (clear ?d)
      (clear ?to))
    :effect (and
      (not (on ?d ?from))
      (on ?d ?to)
      (clear ?from)
      (not (clear ?to))))

  ; Move a clear disk onto a larger clear disk
  (:action move-to-disk
    :parameters (?d - disk ?from - location ?to - disk)
    :precondition (and
      (on ?d ?from)
      (clear ?d)
      (clear ?to)
      (smaller ?d ?to))
    :effect (and
      (not (on ?d ?from))
      (on ?d ?to)
      (clear ?from)
      (not (clear ?to))))
)