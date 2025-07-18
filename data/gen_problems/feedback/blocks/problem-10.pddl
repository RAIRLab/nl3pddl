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
    (ontable b8)
    (on b1 b8)
    (ontable b18)
    (on b6 b18)
    (ontable b17)
    (on b5 b17)
    (ontable b20)
    (on b12 b20)
    (ontable b7)
    (on b16 b7)
    (ontable b10)
    (on b19 b10)
    (ontable b2)
    (on b13 b2)
    (ontable b11)
    (on b9 b11)
    (ontable b15)
    (ontable b3)
    (ontable b4)
    (ontable b14)
    (clear b1)
    (clear b6)
    (clear b5)
    (clear b12)
    (clear b16)
    (clear b19)
    (clear b13)
    (clear b9)
    (clear b15)
    (clear b3)
    (clear b4)
    (clear b14)
    (handempty)
  )

  (:goal (and
    (ontable b13)
    (on b2 b13)
    (ontable b16)
    (on b18 b16)
    (ontable b15)
    (on b10 b15)
    (ontable b14)
    (on b9 b14)
    (ontable b20)
    (on b6 b20)
    (ontable b19)
    (on b17 b19)
    (ontable b12)
    (on b11 b12)
    (ontable b1)
    (on b8 b1)
    (ontable b7)
    (on b5 b7)
    (ontable b3)
    (on b4 b3)
  ))
)
