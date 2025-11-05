(define (domain towers-of-hanoi)
  (:requirements :strips :typing)
  (:types disk peg)

  (:predicates
    (on ?d - disk ?p - peg)          
    (on-top ?d1 - disk ?d2 - disk)   
    (clear-disk ?d - disk)           
    (clear-peg ?p - peg)             
    (smaller ?d1 - disk ?d2 - disk)  
  )

  ; move from peg to peg
  (:action move-peg-to-peg
    :parameters (?d - disk ?from - peg ?to - peg)
    :precondition (and
      (on ?d ?from)
      (clear-disk ?d)
      (clear-peg ?to)
    )
    :effect (and
      (not (on ?d ?from))
      (on ?d ?to)
      (clear-peg ?from)
      (not (clear-peg ?to))
    )
  )

  ; move from disk to peg
  (:action move-disk-to-peg
    :parameters (?d - disk ?below - disk ?to - peg)
    :precondition (and
      (on-top ?d ?below)
      (clear-disk ?d)
      (clear-peg ?to)
    )
    :effect (and
      (not (on-top ?d ?below))
      (not (on ?d ?below))
      (on ?d ?to)
      (clear-disk ?below)
      (not (clear-peg ?to))
    )
  )

  ; move from peg to disk
  (:action move-peg-to-disk
    :parameters (?d - disk ?from - peg ?below - disk)
    :precondition (and
      (on ?d ?from)
      (clear-disk ?d)
      (clear-disk ?below)
      (smaller ?d ?below)
    )
    :effect (and
      (not (on ?d ?from))
      (on-top ?d ?below)
      (on ?d ?below)
      (clear-peg ?from)
      (not (clear-disk ?below))
    )
  )

  ; move disk from disk to disk
  (:action move-disk-to-disk
    :parameters (?d - disk ?from - disk ?to - disk)
    :precondition (and
      (on-top ?d ?from)
      (clear-disk ?d)
      (clear-disk ?to)
      (smaller ?d ?to)
    )
    :effect (and
      (not (on-top ?d ?from))
      (on-top ?d ?to)
      (on ?d ?to)
      (clear-disk ?from)
      (not (clear-disk ?to))
    )
  )
)
