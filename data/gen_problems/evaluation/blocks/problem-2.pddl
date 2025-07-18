(define (problem blocks-prob-2)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )

  (:init
    (ontable b3)
    (on b2 b3)
    (on b1 b2)
    (on b4 b1)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (ontable b1)
    (ontable b4)
    (ontable b3)
  ))
)
