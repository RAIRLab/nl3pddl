(define (problem blocks-prob-1)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )

  (:init
    (ontable b3)
    (on b4 b3)
    (ontable b2)
    (on b1 b2)
    (clear b4)
    (clear b1)
    (handempty)
  )

  (:goal (and
    (ontable b4)
    (on b1 b4)
    (on b3 b1)
    (on b2 b3)
  ))
)
