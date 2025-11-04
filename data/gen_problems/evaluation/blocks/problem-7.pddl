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
    (ontable b9)
    (on b4 b9)
    (ontable b2)
    (ontable b7)
    (ontable b6)
    (ontable b3)
    (ontable b10)
    (ontable b1)
    (ontable b5)
    (ontable b8)
    (clear b4)
    (clear b2)
    (clear b7)
    (clear b6)
    (clear b3)
    (clear b10)
    (clear b1)
    (clear b5)
    (clear b8)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (on b7 b2)
    (ontable b3)
    (on b8 b3)
    (ontable b6)
    (on b1 b6)
    (ontable b10)
    (on b9 b10)
    (ontable b5)
    (ontable b4)
  ))
)
