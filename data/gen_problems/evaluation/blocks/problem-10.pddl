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
    (ontable b13)
    (on b5 b13)
    (ontable b11)
    (on b4 b11)
    (ontable b1)
    (on b10 b1)
    (ontable b2)
    (on b9 b2)
    (ontable b3)
    (ontable b6)
    (ontable b12)
    (ontable b7)
    (ontable b8)
    (clear b5)
    (clear b4)
    (clear b10)
    (clear b9)
    (clear b3)
    (clear b6)
    (clear b12)
    (clear b7)
    (clear b8)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b4 b1)
    (on b12 b4)
    (on b11 b12)
    (on b5 b11)
    (on b2 b5)
    (on b10 b2)
    (on b7 b10)
    (on b9 b7)
    (on b6 b9)
    (on b13 b6)
    (on b3 b13)
    (on b8 b3)
  ))
)
