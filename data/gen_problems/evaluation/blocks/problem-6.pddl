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
    (ontable b9)
    (on b7 b9)
    (ontable b5)
    (on b1 b5)
    (ontable b8)
    (on b2 b8)
    (ontable b6)
    (on b3 b6)
    (ontable b4)
    (clear b7)
    (clear b1)
    (clear b2)
    (clear b3)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b2 b6)
    (ontable b4)
    (on b8 b4)
    (ontable b1)
    (ontable b5)
    (ontable b7)
    (ontable b3)
    (ontable b9)
  ))
)
