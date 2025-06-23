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
    (ontable b10)
    (on b15 b10)
    (ontable b5)
    (on b14 b5)
    (ontable b9)
    (on b4 b9)
    (ontable b17)
    (ontable b1)
    (ontable b16)
    (ontable b13)
    (ontable b6)
    (ontable b7)
    (ontable b8)
    (ontable b18)
    (ontable b3)
    (ontable b2)
    (ontable b12)
    (ontable b11)
    (clear b15)
    (clear b14)
    (clear b4)
    (clear b17)
    (clear b1)
    (clear b16)
    (clear b13)
    (clear b6)
    (clear b7)
    (clear b8)
    (clear b18)
    (clear b3)
    (clear b2)
    (clear b12)
    (clear b11)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b10 b6)
    (on b1 b10)
    (ontable b14)
    (on b3 b14)
    (on b2 b3)
    (ontable b7)
    (on b8 b7)
    (on b5 b8)
    (ontable b18)
    (on b15 b18)
    (on b4 b15)
    (ontable b13)
    (on b11 b13)
    (on b17 b11)
    (ontable b12)
    (on b16 b12)
    (on b9 b16)
  ))
)
