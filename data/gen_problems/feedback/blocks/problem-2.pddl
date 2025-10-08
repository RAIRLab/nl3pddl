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
    (on b3 b4)
    (on b2 b3)
    (on b1 b2)
    (on b5 b1)
    (clear b5)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (on b1 b2)
    (ontable b3)
    (ontable b4)
    (ontable b5)
  ))
)
