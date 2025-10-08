(define (problem blocks-prob-4)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
    b7 - block
  )

  (:init
    (ontable b3)
    (on b7 b3)
    (on b4 b7)
    (ontable b6)
    (on b2 b6)
    (ontable b5)
    (on b1 b5)
    (clear b4)
    (clear b2)
    (clear b1)
    (handempty)
  )

  (:goal (and
    (ontable b5)
    (on b4 b5)
    (ontable b1)
    (ontable b2)
    (ontable b3)
    (ontable b6)
    (ontable b7)
  ))
)
