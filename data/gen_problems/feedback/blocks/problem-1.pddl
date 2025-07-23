(define (problem blocks-prob-1)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
  )

  (:init
    (ontable b4)
    (on b1 b4)
    (ontable b3)
    (ontable b2)
    (clear b1)
    (clear b3)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (on b3 b2)
    (on b4 b3)
    (on b1 b4)
  ))
)
