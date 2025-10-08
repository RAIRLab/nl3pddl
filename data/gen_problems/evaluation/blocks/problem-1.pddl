(define (problem blocks-prob-1)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )

  (:init
    (ontable b2)
    (on b3 b2)
    (ontable b1)
    (on b4 b1)
    (clear b3)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b4 b3)
    (ontable b1)
    (ontable b2)
  ))
)
