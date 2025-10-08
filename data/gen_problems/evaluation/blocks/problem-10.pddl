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
    (ontable b12)
    (on b1 b12)
    (ontable b9)
    (on b2 b9)
    (ontable b13)
    (on b8 b13)
    (ontable b10)
    (on b11 b10)
    (ontable b6)
    (on b4 b6)
    (ontable b7)
    (ontable b5)
    (ontable b3)
    (clear b1)
    (clear b2)
    (clear b8)
    (clear b11)
    (clear b4)
    (clear b7)
    (clear b5)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b4 b6)
    (on b8 b4)
    (ontable b7)
    (on b11 b7)
    (on b3 b11)
    (ontable b12)
    (on b13 b12)
    (on b2 b13)
    (ontable b9)
    (on b1 b9)
    (ontable b5)
    (on b10 b5)
  ))
)
