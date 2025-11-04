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
    (ontable b4)
    (ontable b2)
    (ontable b3)
    (ontable b6)
    (ontable b1)
    (ontable b7)
    (ontable b5)
    (clear b4)
    (clear b2)
    (clear b3)
    (clear b6)
    (clear b1)
    (clear b7)
    (clear b5)
    (handempty)
  )

  (:goal (and
    (ontable b5)
    (on b3 b5)
    (ontable b1)
    (on b2 b1)
    (ontable b4)
    (on b6 b4)
    (ontable b7)
  ))
)
