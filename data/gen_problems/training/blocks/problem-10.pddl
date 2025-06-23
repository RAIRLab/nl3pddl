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
    b14 - block
    b15 - block
    b16 - block
    b17 - block
    b18 - block
    b19 - block
    b20 - block
  )

  (:init
    (ontable b20)
    (on b18 b20)
    (ontable b7)
    (on b16 b7)
    (ontable b10)
    (on b8 b10)
    (ontable b1)
    (ontable b9)
    (ontable b12)
    (ontable b15)
    (ontable b17)
    (ontable b14)
    (ontable b13)
    (ontable b6)
    (ontable b19)
    (ontable b5)
    (ontable b4)
    (ontable b11)
    (ontable b3)
    (ontable b2)
    (clear b18)
    (clear b16)
    (clear b8)
    (clear b1)
    (clear b9)
    (clear b12)
    (clear b15)
    (clear b17)
    (clear b14)
    (clear b13)
    (clear b6)
    (clear b19)
    (clear b5)
    (clear b4)
    (clear b11)
    (clear b3)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b15)
    (on b2 b15)
    (ontable b14)
    (on b1 b14)
    (ontable b5)
    (on b3 b5)
    (ontable b10)
    (on b8 b10)
    (ontable b17)
    (on b4 b17)
    (ontable b20)
    (on b6 b20)
    (ontable b19)
    (on b13 b19)
    (ontable b12)
    (on b16 b12)
    (ontable b7)
    (on b18 b7)
    (ontable b11)
    (on b9 b11)
  ))
)
