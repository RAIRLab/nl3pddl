(define (problem blocks-prob-7)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
    b7 - block
    b8 - block
    b9 - block
    b10 - block
  )

  (:init
    (ontable b10)
    (ontable b1)
    (ontable b8)
    (ontable b7)
    (ontable b9)
    (ontable b2)
    (ontable b6)
    (ontable b4)
    (ontable b5)
    (ontable b3)
    (clear b10)
    (clear b1)
    (clear b8)
    (clear b7)
    (clear b9)
    (clear b2)
    (clear b6)
    (clear b4)
    (clear b5)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b4 b1)
    (ontable b9)
    (ontable b2)
    (ontable b8)
    (ontable b7)
    (ontable b10)
    (ontable b6)
    (ontable b5)
    (ontable b3)
  ))
)
