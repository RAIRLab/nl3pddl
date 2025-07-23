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
    (ontable b6)
    (on b2 b6)
    (on b11 b2)
    (on b1 b11)
    (ontable b8)
    (on b7 b8)
    (on b9 b7)
    (on b5 b9)
    (ontable b4)
    (on b10 b4)
    (on b3 b10)
    (clear b1)
    (clear b5)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b11)
    (on b2 b11)
    (ontable b3)
    (on b7 b3)
    (ontable b4)
    (on b6 b4)
    (ontable b8)
    (on b10 b8)
    (ontable b9)
    (ontable b5)
    (ontable b1)
  ))
)
