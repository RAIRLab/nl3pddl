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
    (ontable b2)
    (on b1 b2)
    (on b4 b1)
    (on b6 b4)
    (on b5 b6)
    (on b3 b5)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b4)
    (on b6 b4)
    (ontable b2)
    (ontable b5)
    (ontable b1)
    (ontable b3)
  ))
)
