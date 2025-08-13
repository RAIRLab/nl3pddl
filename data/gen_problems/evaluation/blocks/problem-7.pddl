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
    (ontable b6)
    (on b2 b6)
    (ontable b5)
    (on b10 b5)
    (ontable b7)
    (on b4 b7)
    (ontable b1)
    (on b9 b1)
    (ontable b3)
    (on b8 b3)
    (clear b2)
    (clear b10)
    (clear b4)
    (clear b9)
    (clear b8)
    (handempty)
  )

  (:goal (and
    (ontable b8)
    (on b1 b8)
    (ontable b7)
    (on b6 b7)
    (ontable b2)
    (on b5 b2)
    (ontable b4)
    (ontable b10)
    (ontable b9)
    (ontable b3)
  ))
)
