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
    (ontable b9)
    (on b4 b9)
    (on b3 b4)
    (on b6 b3)
    (ontable b10)
    (on b8 b10)
    (on b7 b8)
    (ontable b5)
    (on b2 b5)
    (on b1 b2)
    (clear b6)
    (clear b7)
    (clear b1)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b6 b3)
    (on b9 b6)
    (on b4 b9)
    (on b2 b4)
    (ontable b8)
    (on b1 b8)
    (on b10 b1)
    (on b5 b10)
    (on b7 b5)
  ))
)
