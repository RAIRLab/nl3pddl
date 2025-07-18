(define (problem blocks-prob-2)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )

  (:init
    (ontable b1)
    (on b2 b1)
    (ontable b4)
    (on b3 b4)
    (clear b2)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (ontable b1)
    (ontable b4)
    (ontable b3)
  ))
)
