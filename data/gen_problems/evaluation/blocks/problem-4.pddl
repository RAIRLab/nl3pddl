(define (problem blocks-prob-4)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
    b7 - block
  )

  (:init
    (ontable b6)
    (on b1 b6)
    (ontable b7)
    (ontable b5)
    (ontable b3)
    (ontable b4)
    (ontable b2)
    (clear b1)
    (clear b7)
    (clear b5)
    (clear b3)
    (clear b4)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b6 b1)
    (ontable b4)
    (on b7 b4)
    (ontable b3)
    (ontable b5)
    (ontable b2)
  ))
)
