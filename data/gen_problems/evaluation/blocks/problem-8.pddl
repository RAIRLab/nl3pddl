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
  )

  (:init
    (ontable b8)
    (on b4 b8)
    (on b1 b4)
    (on b11 b1)
    (on b6 b11)
    (on b2 b6)
    (on b3 b2)
    (on b7 b3)
    (on b10 b7)
    (on b5 b10)
    (on b9 b5)
    (clear b9)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b4 b3)
    (on b7 b4)
    (ontable b5)
    (on b2 b5)
    (on b11 b2)
    (ontable b10)
    (on b1 b10)
    (on b9 b1)
    (ontable b8)
    (on b6 b8)
  ))
)
