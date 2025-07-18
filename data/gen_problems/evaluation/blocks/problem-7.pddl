(define (problem blocks-prob-7)
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
  )

  (:init
    (ontable b4)
    (on b2 b4)
    (ontable b3)
    (on b7 b3)
    (ontable b10)
    (on b1 b10)
    (ontable b5)
    (on b12 b5)
    (ontable b9)
    (on b11 b9)
    (ontable b13)
    (on b8 b13)
    (ontable b14)
    (on b6 b14)
    (clear b2)
    (clear b7)
    (clear b1)
    (clear b12)
    (clear b11)
    (clear b8)
    (clear b6)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b4 b1)
    (on b14 b4)
    (ontable b7)
    (on b12 b7)
    (on b13 b12)
    (ontable b11)
    (on b10 b11)
    (on b3 b10)
    (ontable b5)
    (on b2 b5)
    (on b6 b2)
    (ontable b8)
    (on b9 b8)
  ))
)
