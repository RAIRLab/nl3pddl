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
    (ontable b1)
    (on b13 b1)
    (ontable b4)
    (on b8 b4)
    (ontable b9)
    (on b6 b9)
    (ontable b12)
    (on b11 b12)
    (ontable b2)
    (ontable b7)
    (ontable b5)
    (ontable b3)
    (ontable b10)
    (clear b13)
    (clear b8)
    (clear b6)
    (clear b11)
    (clear b2)
    (clear b7)
    (clear b5)
    (clear b3)
    (clear b10)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b7 b1)
    (ontable b2)
    (on b3 b2)
    (ontable b4)
    (on b8 b4)
    (ontable b9)
    (on b12 b9)
    (ontable b11)
    (ontable b13)
    (ontable b10)
    (ontable b5)
    (ontable b6)
  ))
)
