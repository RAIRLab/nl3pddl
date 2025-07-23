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
    (ontable b8)
    (on b9 b8)
    (ontable b10)
    (on b3 b10)
    (ontable b5)
    (on b4 b5)
    (ontable b2)
    (on b1 b2)
    (ontable b6)
    (ontable b7)
    (clear b9)
    (clear b3)
    (clear b4)
    (clear b1)
    (clear b6)
    (clear b7)
    (handempty)
  )

  (:goal (and
    (ontable b7)
    (on b5 b7)
    (on b1 b5)
    (on b4 b1)
    (on b6 b4)
    (on b10 b6)
    (on b9 b10)
    (on b8 b9)
    (on b3 b8)
    (on b2 b3)
  ))
)
