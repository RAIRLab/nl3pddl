(define (problem sliding-puzzle-2x2)
  (:domain sliding-puzzle)

  (:objects
    t1 t2 t3 - tile
    p11 p12 p21 p22 - position
  )

  (:init
    (at t2 p11)
    (at t3 p12)
    (at t1 p21)
    (empty p22)

    (adjacent p11 p12)
    (adjacent p11 p21)
    (adjacent p12 p11)
    (adjacent p12 p22)
    (adjacent p21 p11)
    (adjacent p21 p22)
    (adjacent p22 p12)
    (adjacent p22 p21)
  )

  (:goal
    (and
      (at t1 p11)
      (at t2 p12)
      (at t3 p21)
      (empty p22)
    )
  )
)
