(define (problem hanoi-4)
  (:domain towers-of-hanoi)

  (:objects
    d1 d2 d3 d4 - disk
    peg1 peg2 peg3 - peg
  )

  (:init
    (smaller d2 d1)
    (smaller d3 d1)
    (smaller d4 d1)
    (smaller d3 d2)
    (smaller d4 d2)
    (smaller d4 d3)

    (on d1 peg1)
    (on-top d2 d1)
    (on d2 d1)
    (on-top d3 d2)
    (on d3 d2)
    (on-top d4 d3)
    (on d4 d3)
    (clear-disk d4)
    (clear-peg peg2)
    (clear-peg peg3)
  )

  (:goal
    (and
      (on d1 peg3)
      (on-top d2 d1)
      (on d2 d1)
      (on-top d3 d2)
      (on d3 d2)
      (on-top d4 d3)
      (on d4 d3)
      (clear-disk d4)
    )
  )
)
