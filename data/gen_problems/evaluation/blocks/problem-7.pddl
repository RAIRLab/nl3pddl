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
  )

  (:init
    (ontable b7)
    (on b2 b7)
    (on b4 b2)
    (on b10 b4)
    (on b5 b10)
    (ontable b1)
    (on b6 b1)
    (on b9 b6)
    (on b8 b9)
    (on b3 b8)
    (clear b5)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b8)
    (on b7 b8)
    (ontable b6)
    (on b5 b6)
    (ontable b4)
    (on b10 b4)
    (ontable b1)
    (on b2 b1)
    (ontable b3)
    (ontable b9)
  ))
)
