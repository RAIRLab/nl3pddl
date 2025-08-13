(define (problem blocks-prob-9)
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
    b11 - block
    b12 - block
  )

  (:init
    (ontable b1)
    (on b12 b1)
    (ontable b6)
    (on b8 b6)
    (ontable b2)
    (ontable b3)
    (ontable b10)
    (ontable b5)
    (ontable b7)
    (ontable b9)
    (ontable b4)
    (ontable b11)
    (clear b12)
    (clear b8)
    (clear b2)
    (clear b3)
    (clear b10)
    (clear b5)
    (clear b7)
    (clear b9)
    (clear b4)
    (clear b11)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (ontable b11)
    (ontable b8)
    (ontable b7)
    (ontable b12)
    (ontable b2)
    (ontable b4)
    (ontable b1)
    (ontable b9)
    (ontable b6)
    (ontable b5)
    (ontable b10)
  ))
)
