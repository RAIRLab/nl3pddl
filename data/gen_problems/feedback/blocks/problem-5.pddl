(define (problem blocks-prob-5)
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
    (ontable b3)
    (on b4 b3)
    (on b1 b4)
    (on b2 b1)
    (on b7 b2)
    (ontable b8)
    (on b10 b8)
    (on b6 b10)
    (on b5 b6)
    (on b9 b5)
    (clear b7)
    (clear b9)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b3 b1)
    (ontable b2)
    (on b4 b2)
    (ontable b6)
    (on b8 b6)
    (ontable b9)
    (on b7 b9)
    (ontable b10)
    (ontable b5)
  ))
)
