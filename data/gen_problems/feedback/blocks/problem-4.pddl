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
    (ontable b2)
    (on b6 b2)
    (ontable b5)
    (ontable b4)
    (ontable b7)
    (clear b3)
    (clear b6)
    (clear b5)
    (clear b4)
    (clear b7)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b2 b6)
    (on b7 b2)
    (on b5 b7)
    (on b4 b5)
    (on b3 b4)
    (on b1 b3)
  ))
)
