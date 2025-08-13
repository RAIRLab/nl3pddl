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
    (ontable b5)
    (on b2 b5)
    (ontable b7)
    (on b1 b7)
    (ontable b3)
    (on b6 b3)
    (ontable b8)
    (on b4 b8)
    (ontable b9)
    (clear b2)
    (clear b1)
    (clear b6)
    (clear b4)
    (clear b9)
    (handempty)
  )

  (:goal (and
    (ontable b9)
    (on b6 b9)
    (on b7 b6)
    (on b2 b7)
    (on b3 b2)
    (on b1 b3)
    (on b5 b1)
    (on b4 b5)
    (on b8 b4)
  ))
)
