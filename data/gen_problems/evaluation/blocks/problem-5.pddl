(define (problem blocks-prob-5)
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
    (on b8 b4)
    (on b1 b8)
    (ontable b7)
    (on b2 b7)
    (on b6 b2)
    (ontable b3)
    (on b5 b3)
    (clear b1)
    (clear b6)
    (clear b5)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b5 b3)
    (ontable b1)
    (ontable b4)
    (ontable b2)
    (ontable b8)
    (ontable b7)
    (ontable b6)
  ))
)
