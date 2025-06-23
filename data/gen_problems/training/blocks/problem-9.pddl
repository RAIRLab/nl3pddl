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
    b13 - block
    b14 - block
    b15 - block
    b16 - block
    b17 - block
    b18 - block
  )

  (:init
    (ontable b1)
    (on b9 b1)
    (on b7 b9)
    (ontable b16)
    (on b14 b16)
    (on b4 b14)
    (ontable b3)
    (on b8 b3)
    (on b5 b8)
    (ontable b18)
    (on b13 b18)
    (on b12 b13)
    (ontable b6)
    (on b2 b6)
    (ontable b11)
    (on b10 b11)
    (ontable b17)
    (on b15 b17)
    (clear b7)
    (clear b4)
    (clear b5)
    (clear b12)
    (clear b2)
    (clear b10)
    (clear b15)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (ontable b7)
    (ontable b13)
    (ontable b6)
    (ontable b8)
    (ontable b9)
    (ontable b16)
    (ontable b4)
    (ontable b15)
    (ontable b3)
    (ontable b2)
    (ontable b5)
    (ontable b18)
    (ontable b12)
    (ontable b11)
    (ontable b14)
    (ontable b10)
    (ontable b17)
  ))
)
