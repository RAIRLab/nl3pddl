(define (problem blocks-prob-4)
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
  )

  (:init
    (ontable b7)
    (on b2 b7)
    (ontable b5)
    (on b6 b5)
    (ontable b1)
    (on b4 b1)
    (ontable b8)
    (on b3 b8)
    (clear b2)
    (clear b6)
    (clear b4)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b2 b6)
    (ontable b3)
    (on b4 b3)
    (ontable b1)
    (on b7 b1)
    (ontable b5)
    (on b8 b5)
  ))
)
