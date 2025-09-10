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
    (ontable b9)
    (on b3 b9)
    (ontable b10)
    (ontable b1)
    (ontable b6)
    (ontable b5)
    (ontable b4)
    (ontable b2)
    (ontable b7)
    (ontable b11)
    (ontable b8)
    (clear b3)
    (clear b10)
    (clear b1)
    (clear b6)
    (clear b5)
    (clear b4)
    (clear b2)
    (clear b7)
    (clear b11)
    (clear b8)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b4 b1)
    (on b8 b4)
    (on b11 b8)
    (on b7 b11)
    (on b9 b7)
    (ontable b6)
    (on b3 b6)
    (on b2 b3)
    (on b10 b2)
    (on b5 b10)
  ))
)
