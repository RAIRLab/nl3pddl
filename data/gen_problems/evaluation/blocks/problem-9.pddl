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
  )

  (:init
    (ontable b4)
    (on b12 b4)
    (on b3 b12)
    (ontable b6)
    (on b11 b6)
    (on b10 b11)
    (ontable b1)
    (on b8 b1)
    (on b7 b8)
    (ontable b2)
    (on b5 b2)
    (on b9 b5)
    (clear b3)
    (clear b10)
    (clear b7)
    (clear b9)
    (handempty)
  )

  (:goal (and
    (ontable b10)
    (on b5 b10)
    (on b7 b5)
    (on b9 b7)
    (on b3 b9)
    (on b11 b3)
    (ontable b4)
    (on b2 b4)
    (on b12 b2)
    (on b8 b12)
    (on b6 b8)
    (on b1 b6)
  ))
)
