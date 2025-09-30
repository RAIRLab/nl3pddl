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
    (on b2 b1)
    (ontable b5)
    (on b3 b5)
    (ontable b4)
    (ontable b7)
    (ontable b6)
    (clear b2)
    (clear b3)
    (clear b4)
    (clear b7)
    (clear b6)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b3 b6)
    (on b4 b3)
    (on b2 b4)
    (on b5 b2)
    (on b1 b5)
    (on b7 b1)
  ))
)
