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
    (ontable b10)
    (ontable b6)
    (ontable b4)
    (ontable b16)
    (ontable b2)
    (ontable b5)
    (ontable b9)
    (ontable b12)
    (ontable b15)
    (ontable b11)
    (ontable b1)
    (ontable b8)
    (ontable b3)
    (ontable b13)
    (ontable b14)
    (ontable b7)
    (clear b10)
    (clear b6)
    (clear b4)
    (clear b16)
    (clear b2)
    (clear b5)
    (clear b9)
    (clear b12)
    (clear b15)
    (clear b11)
    (clear b1)
    (clear b8)
    (clear b3)
    (clear b13)
    (clear b14)
    (clear b7)
    (handempty)
  )

  (:goal (and
    (ontable b10)
    (on b1 b10)
    (on b3 b1)
    (ontable b14)
    (on b15 b14)
    (on b5 b15)
    (ontable b9)
    (on b13 b9)
    (ontable b4)
    (on b8 b4)
    (ontable b6)
    (on b7 b6)
    (ontable b12)
    (on b11 b12)
    (ontable b16)
    (on b2 b16)
  ))
)
