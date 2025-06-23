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
    (ontable b1)
    (on b9 b1)
    (on b8 b9)
    (on b6 b8)
    (on b2 b6)
    (on b12 b2)
    (ontable b7)
    (on b5 b7)
    (on b4 b5)
    (on b3 b4)
    (on b10 b3)
    (on b11 b10)
    (clear b12)
    (clear b11)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b12 b3)
    (ontable b11)
    (ontable b9)
    (ontable b10)
    (ontable b1)
    (ontable b7)
    (ontable b6)
    (ontable b2)
    (ontable b5)
    (ontable b4)
    (ontable b8)
  ))
)
