(define (problem lights_out_6)
  (:domain lights-out-strips)
  (:objects
    b1 - bubble
    b2 - bubble
    b3 - bubble
    b4 - bubble
    b5 - bubble
    b6 - bubble
  )
  (:init
    (off b1)
    (off b2)
    (off b3)
    (on b4)
    (on b5)
    (off b6)
    (connected b1 b2)
    (connected b1 b4)
    (connected b2 b1)
    (connected b2 b6)
    (connected b2 b3)
    (connected b3 b5)
    (connected b3 b2)
    (connected b4 b1)
    (connected b4 b6)
    (connected b4 b5)
    (connected b5 b6)
    (connected b5 b3)
    (connected b5 b4)
    (connected b6 b5)
    (connected b6 b2)
    (connected b6 b4)
    (two-neighbors b1)
    (three-neighbors b2)
    (two-neighbors b3)
    (three-neighbors b4)
    (three-neighbors b5)
    (three-neighbors b6)
  )
  (:goal (and
    (off b1)
    (off b2)
    (off b3)
    (off b4)
    (off b5)
    (off b6)
  ))
)
