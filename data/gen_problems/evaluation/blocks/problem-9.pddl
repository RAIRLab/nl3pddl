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
    (ontable b6)
    (ontable b7)
    (ontable b3)
    (ontable b10)
    (ontable b11)
    (ontable b5)
    (ontable b2)
    (ontable b9)
    (ontable b12)
    (ontable b8)
    (clear b1)
    (clear b6)
    (clear b7)
    (clear b3)
    (clear b10)
    (clear b11)
    (clear b5)
    (clear b2)
    (clear b9)
    (clear b12)
    (clear b8)
    (handempty)
  )

  (:goal (and
    (ontable b8)
    (on b6 b8)
    (on b10 b6)
    (ontable b1)
    (on b11 b1)
    (on b9 b11)
    (ontable b4)
    (on b2 b4)
    (ontable b3)
    (on b5 b3)
    (ontable b12)
    (on b7 b12)
  ))
)
