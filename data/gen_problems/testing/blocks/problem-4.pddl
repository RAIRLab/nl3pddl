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
    b8 - block
  )

  (:init
    (ontable b4)
    (on b1 b4)
    (ontable b5)
    (ontable b3)
    (ontable b7)
    (ontable b2)
    (ontable b8)
    (ontable b6)
    (clear b1)
    (clear b5)
    (clear b3)
    (clear b7)
    (clear b2)
    (clear b8)
    (clear b6)
    (handempty)
  )

  (:goal (and
    (ontable b5)
    (on b6 b5)
    (on b7 b6)
    (on b8 b7)
    (ontable b4)
    (on b1 b4)
    (on b2 b1)
    (on b3 b2)
  ))
)
