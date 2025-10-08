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
  )

  (:init
    (ontable b6)
    (on b5 b6)
    (ontable b1)
    (on b7 b1)
    (ontable b2)
    (ontable b3)
    (ontable b4)
    (clear b5)
    (clear b7)
    (clear b2)
    (clear b3)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b3 b6)
    (ontable b2)
    (on b1 b2)
    (ontable b7)
    (ontable b5)
    (ontable b4)
  ))
)
