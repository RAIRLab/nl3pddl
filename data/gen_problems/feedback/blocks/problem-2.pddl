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
    (ontable b2)
    (on b3 b2)
    (ontable b1)
    (on b5 b1)
    (ontable b4)
    (clear b3)
    (clear b5)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b1 b3)
    (ontable b4)
    (ontable b2)
    (ontable b5)
  ))
)
