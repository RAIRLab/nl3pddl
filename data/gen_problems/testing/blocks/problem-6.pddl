(define (problem blocks-prob-6)
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
    (ontable b7)
    (on b5 b7)
    (on b4 b5)
    (ontable b8)
    (on b12 b8)
    (on b9 b12)
    (ontable b6)
    (on b11 b6)
    (on b1 b11)
    (ontable b2)
    (on b3 b2)
    (on b10 b3)
    (clear b4)
    (clear b9)
    (clear b1)
    (clear b10)
    (handempty)
  )

  (:goal (and
    (ontable b11)
    (on b10 b11)
    (ontable b8)
    (on b7 b8)
    (ontable b3)
    (on b6 b3)
    (ontable b2)
    (on b12 b2)
    (ontable b4)
    (on b5 b4)
    (ontable b1)
    (ontable b9)
  ))
)
