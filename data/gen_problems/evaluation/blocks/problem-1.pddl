(define (problem blocks-prob-1)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
  )

  (:init
    (ontable b2)
    (on b1 b2)
    (clear b1)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (on b1 b2)
  ))
)
