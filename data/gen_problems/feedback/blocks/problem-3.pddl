(define (problem blocks-prob-3)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
  )

  (:init
    (ontable b5)
    (on b1 b5)
    (ontable b3)
    (ontable b2)
    (ontable b4)
    (ontable b6)
    (clear b1)
    (clear b3)
    (clear b2)
    (clear b4)
    (clear b6)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b5 b3)
    (ontable b1)
    (on b4 b1)
    (ontable b6)
    (ontable b2)
  ))
)
