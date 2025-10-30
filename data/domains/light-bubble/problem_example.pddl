(define (problem lights_out_4_7)
  (:domain lights-out-strips)
  (:objects
    b1 - bubble
    b2 - bubble
    b3 - bubble
    b4 - bubble
  )
  (:init
    (off b1)
    (off b2)
    (off b3)
    (off b4)
    (connected b1 b4)
    (connected b1 b2)
    (connected b1 b3)
    (connected b2 b1)
    (connected b2 b3)
    (connected b3 b4)
    (connected b3 b1)
    (connected b3 b2)
    (connected b4 b1)
    (connected b4 b3)
    (three-neighbors b1)
    (two-neighbors b2)
    (three-neighbors b3)
    (two-neighbors b4)
  )
  (:goal (and
    (off b1)
    (off b2)
    (off b3)
    (off b4)
  ))
)
