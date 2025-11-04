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
    (on b1 b3)
    (ontable b5)
    (ontable b2)
    (ontable b4)
    (clear b1)
    (clear b5)
    (clear b2)
    (clear b4)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b2 b3)
    (ontable b5)
    (on b1 b5)
    (ontable b4)
  ))
)
