(define (problem blocks-prob-10)
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
    b13 - block
  )

  (:init
    (ontable b11)
    (on b12 b11)
    (ontable b4)
    (on b6 b4)
    (ontable b13)
    (ontable b5)
    (ontable b7)
    (ontable b10)
    (ontable b1)
    (ontable b2)
    (ontable b8)
    (ontable b3)
    (ontable b9)
    (clear b12)
    (clear b6)
    (clear b13)
    (clear b5)
    (clear b7)
    (clear b10)
    (clear b1)
    (clear b2)
    (clear b8)
    (clear b3)
    (clear b9)
    (handempty)
  )

  (:goal (and
    (ontable b13)
    (on b7 b13)
    (ontable b4)
    (on b12 b4)
    (ontable b11)
    (on b3 b11)
    (ontable b8)
    (on b5 b8)
    (ontable b10)
    (on b6 b10)
    (ontable b1)
    (on b2 b1)
    (ontable b9)
  ))
)
