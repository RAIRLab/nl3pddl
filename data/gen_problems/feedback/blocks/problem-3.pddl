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
    (on b3 b5)
    (on b6 b3)
    (ontable b4)
    (on b1 b4)
    (on b2 b1)
    (clear b6)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b4)
    (on b5 b4)
    (ontable b2)
    (on b6 b2)
    (ontable b3)
    (ontable b1)
  ))
)
