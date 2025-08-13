(define (problem blocks-prob-8)
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
  )

  (:init
    (ontable b8)
    (on b6 b8)
    (ontable b9)
    (ontable b3)
    (ontable b5)
    (ontable b4)
    (ontable b11)
    (ontable b2)
    (ontable b10)
    (ontable b1)
    (ontable b7)
    (clear b6)
    (clear b9)
    (clear b3)
    (clear b5)
    (clear b4)
    (clear b11)
    (clear b2)
    (clear b10)
    (clear b1)
    (clear b7)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (ontable b1)
    (ontable b4)
    (ontable b10)
    (ontable b5)
    (ontable b2)
    (ontable b6)
    (ontable b9)
    (ontable b8)
    (ontable b11)
    (ontable b7)
  ))
)
