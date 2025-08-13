(define (problem blocks-prob-2)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
  )

  (:init
    (ontable b3)
    (ontable b2)
    (ontable b5)
    (ontable b1)
    (ontable b4)
    (clear b3)
    (clear b2)
    (clear b5)
    (clear b1)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b4 b3)
    (ontable b2)
    (on b5 b2)
    (ontable b1)
  ))
)
