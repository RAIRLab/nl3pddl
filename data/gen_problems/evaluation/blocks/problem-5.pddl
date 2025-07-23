(define (problem blocks-prob-5)
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
    (ontable b8)
    (on b2 b8)
    (ontable b6)
    (on b7 b6)
    (ontable b3)
    (ontable b1)
    (ontable b5)
    (ontable b4)
    (clear b2)
    (clear b7)
    (clear b3)
    (clear b1)
    (clear b5)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b2 b6)
    (ontable b3)
    (on b8 b3)
    (ontable b4)
    (ontable b1)
    (ontable b7)
    (ontable b5)
  ))
)
