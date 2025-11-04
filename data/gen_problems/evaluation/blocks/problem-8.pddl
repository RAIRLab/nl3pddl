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
    (ontable b7)
    (on b6 b7)
    (ontable b8)
    (on b3 b8)
    (ontable b2)
    (on b9 b2)
    (ontable b1)
    (ontable b11)
    (ontable b10)
    (ontable b4)
    (ontable b5)
    (clear b6)
    (clear b3)
    (clear b9)
    (clear b1)
    (clear b11)
    (clear b10)
    (clear b4)
    (clear b5)
    (handempty)
  )

  (:goal (and
    (ontable b9)
    (on b6 b9)
    (on b3 b6)
    (ontable b8)
    (on b2 b8)
    (on b11 b2)
    (ontable b4)
    (on b10 b4)
    (on b7 b10)
    (ontable b5)
    (on b1 b5)
  ))
)
