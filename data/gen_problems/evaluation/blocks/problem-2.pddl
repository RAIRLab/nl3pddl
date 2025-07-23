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
    (ontable b4)
    (on b5 b4)
    (on b1 b5)
    (ontable b3)
    (on b2 b3)
    (clear b1)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b2 b3)
    (ontable b5)
    (ontable b1)
    (ontable b4)
  ))
)
