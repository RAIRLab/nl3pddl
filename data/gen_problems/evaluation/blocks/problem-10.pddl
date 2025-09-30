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
    (ontable b2)
    (on b4 b2)
    (on b8 b4)
    (on b13 b8)
    (ontable b11)
    (on b3 b11)
    (on b10 b3)
    (ontable b5)
    (on b12 b5)
    (on b9 b12)
    (ontable b6)
    (on b1 b6)
    (on b7 b1)
    (clear b13)
    (clear b10)
    (clear b9)
    (clear b7)
    (handempty)
  )

  (:goal (and
    (ontable b11)
    (on b3 b11)
    (on b8 b3)
    (ontable b9)
    (on b13 b9)
    (ontable b6)
    (on b2 b6)
    (ontable b7)
    (on b4 b7)
    (ontable b10)
    (on b1 b10)
    (ontable b5)
    (on b12 b5)
  ))
)
