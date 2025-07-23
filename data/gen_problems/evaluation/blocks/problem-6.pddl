(define (problem blocks-prob-6)
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
  )

  (:init
    (ontable b6)
    (on b1 b6)
    (on b4 b1)
    (ontable b8)
    (on b5 b8)
    (on b3 b5)
    (ontable b7)
    (on b9 b7)
    (on b2 b9)
    (clear b4)
    (clear b3)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b5)
    (on b4 b5)
    (on b7 b4)
    (ontable b1)
    (on b2 b1)
    (on b9 b2)
    (ontable b6)
    (on b3 b6)
    (on b8 b3)
  ))
)
