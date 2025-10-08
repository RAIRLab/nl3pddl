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
    (ontable b1)
    (on b3 b1)
    (ontable b5)
    (ontable b6)
    (ontable b4)
    (ontable b2)
    (clear b3)
    (clear b5)
    (clear b6)
    (clear b4)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b5)
    (on b3 b5)
    (ontable b2)
    (on b4 b2)
    (ontable b1)
    (on b6 b1)
  ))
)
