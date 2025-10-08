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
    (ontable b5)
    (on b8 b5)
    (on b4 b8)
    (on b1 b4)
    (on b6 b1)
    (on b2 b6)
    (on b7 b2)
    (on b10 b7)
    (on b3 b10)
    (on b11 b3)
    (on b9 b11)
    (on b12 b9)
    (clear b12)
    (handempty)
  )

  (:goal (and
    (ontable b10)
    (on b3 b10)
    (on b9 b3)
    (on b7 b9)
    (on b12 b7)
    (on b6 b12)
    (on b8 b6)
    (on b2 b8)
    (on b1 b2)
    (on b5 b1)
    (on b4 b5)
    (on b11 b4)
  ))
)
