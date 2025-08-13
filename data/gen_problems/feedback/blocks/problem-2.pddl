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
    (on b2 b5)
    (on b1 b2)
    (on b3 b1)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b5 b1)
    (on b3 b5)
    (ontable b2)
    (on b4 b2)
  ))
)
