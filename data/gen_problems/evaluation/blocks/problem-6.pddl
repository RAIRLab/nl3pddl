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
    (on b5 b6)
    (on b7 b5)
    (ontable b3)
    (on b9 b3)
    (on b1 b9)
    (ontable b8)
    (on b4 b8)
    (on b2 b4)
    (clear b7)
    (clear b1)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b7 b6)
    (ontable b3)
    (ontable b5)
    (ontable b9)
    (ontable b2)
    (ontable b8)
    (ontable b4)
    (ontable b1)
  ))
)
