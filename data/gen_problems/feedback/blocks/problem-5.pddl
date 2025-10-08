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
    (ontable b2)
    (on b1 b2)
    (ontable b8)
    (on b7 b8)
    (ontable b4)
    (on b6 b4)
    (ontable b5)
    (ontable b3)
    (clear b1)
    (clear b7)
    (clear b6)
    (clear b5)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b8)
    (on b3 b8)
    (ontable b5)
    (on b6 b5)
    (ontable b7)
    (ontable b4)
    (ontable b1)
    (ontable b2)
  ))
)
