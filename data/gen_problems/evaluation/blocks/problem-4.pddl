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
    (ontable b1)
    (on b3 b1)
    (ontable b7)
    (on b6 b7)
    (ontable b5)
    (on b4 b5)
    (ontable b2)
    (clear b3)
    (clear b6)
    (clear b4)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b1)
    (on b3 b1)
    (on b5 b3)
    (on b7 b5)
    (on b6 b7)
    (on b4 b6)
    (on b2 b4)
  ))
)
