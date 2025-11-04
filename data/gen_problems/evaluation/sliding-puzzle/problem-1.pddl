(define (problem sliding-puzzle-1x1)
  (:domain sliding-puzzle)

  (:objects
    p11 - position
  )

  (:init
    (empty p11)

  )

  (:goal
    (and
      (empty p11)
    )
  )
)
