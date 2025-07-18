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
    b12 - block
    b13 - block
    b14 - block
    b15 - block
    b16 - block
  )

  (:init
    (ontable b14)
    (ontable b4)
    (ontable b10)
    (ontable b15)
    (ontable b11)
    (ontable b6)
    (ontable b16)
    (ontable b7)
    (ontable b1)
    (ontable b12)
    (ontable b8)
    (ontable b3)
    (ontable b13)
    (ontable b9)
    (ontable b2)
    (ontable b5)
    (clear b14)
    (clear b4)
    (clear b10)
    (clear b15)
    (clear b11)
    (clear b6)
    (clear b16)
    (clear b7)
    (clear b1)
    (clear b12)
    (clear b8)
    (clear b3)
    (clear b13)
    (clear b9)
    (clear b2)
    (clear b5)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b15 b1)
    (on b6 b15)
    (on b16 b6)
    (on b10 b16)
    (on b5 b10)
    (on b9 b5)
    (on b2 b9)
    (on b3 b2)
    (on b4 b3)
    (on b7 b4)
    (on b8 b7)
    (on b11 b8)
    (on b12 b11)
    (on b14 b12)
    (on b13 b14)
  ))
)
