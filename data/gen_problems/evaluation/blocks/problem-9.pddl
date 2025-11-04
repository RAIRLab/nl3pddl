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
    (on b1 b4)
    (on b8 b1)
    (ontable b2)
    (on b3 b2)
    (on b9 b3)
    (ontable b5)
    (on b7 b5)
    (ontable b10)
    (on b11 b10)
    (ontable b6)
    (on b12 b6)
    (clear b8)
    (clear b9)
    (clear b7)
    (clear b11)
    (clear b12)
    (handempty)
  )

  (:goal (and
    (ontable b9)
    (on b3 b9)
    (on b4 b3)
    (ontable b1)
    (on b5 b1)
    (on b10 b5)
    (ontable b6)
    (on b11 b6)
    (on b12 b11)
    (ontable b2)
    (on b7 b2)
    (on b8 b7)
  ))
)
