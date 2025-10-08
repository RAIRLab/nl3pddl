(define (problem blocks-prob-1)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )

  (:init
    (ontable b4)
    (ontable b3)
    (ontable b1)
    (ontable b2)
    (clear b4)
    (clear b3)
    (clear b1)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b2 b3)
    (ontable b4)
    (on b1 b4)
  ))
)
