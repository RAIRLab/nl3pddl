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
    (ontable b6)
    (on b5 b6)
    (ontable b8)
    (on b3 b8)
    (ontable b1)
    (on b12 b1)
    (ontable b14)
    (on b13 b14)
    (ontable b2)
    (on b7 b2)
    (ontable b9)
    (on b10 b9)
    (ontable b11)
    (ontable b4)
    (clear b5)
    (clear b3)
    (clear b12)
    (clear b13)
    (clear b7)
    (clear b10)
    (clear b11)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b8 b6)
    (on b13 b8)
    (on b10 b13)
    (ontable b5)
    (on b4 b5)
    (on b7 b4)
    (on b9 b7)
    (ontable b12)
    (on b1 b12)
    (on b3 b1)
    (ontable b14)
    (on b2 b14)
    (on b11 b2)
  ))
)
