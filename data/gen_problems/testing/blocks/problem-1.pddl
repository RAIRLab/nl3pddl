(define (problem blocks-prob-1)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
  )

  (:init
    (ontable b2)
    (ontable b1)
    (clear b2)
    (clear b1)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b2 b1)
  ))
)
