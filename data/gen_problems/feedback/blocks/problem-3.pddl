(define (problem blocks-prob-3)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
  )

  (:init
    (ontable b2)
    (on b3 b2)
    (on b6 b3)
    (ontable b5)
    (on b1 b5)
    (on b4 b1)
    (clear b6)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b6 b1)
    (ontable b5)
    (ontable b2)
    (ontable b4)
    (ontable b3)
  ))
)
