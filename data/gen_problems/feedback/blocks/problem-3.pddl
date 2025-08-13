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
    (ontable b4)
    (on b2 b4)
    (on b5 b2)
    (on b3 b5)
    (on b6 b3)
    (on b1 b6)
    (clear b1)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b5 b1)
    (ontable b3)
    (on b6 b3)
    (ontable b4)
    (on b2 b4)
  ))
)
