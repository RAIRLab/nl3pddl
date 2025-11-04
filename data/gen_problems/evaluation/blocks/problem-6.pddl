(define (problem blocks-prob-6)
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
    b9 - block
  )

  (:init
    (ontable b2)
    (on b6 b2)
    (ontable b5)
    (ontable b9)
    (ontable b7)
    (ontable b3)
    (ontable b1)
    (ontable b4)
    (ontable b8)
    (clear b6)
    (clear b5)
    (clear b9)
    (clear b7)
    (clear b3)
    (clear b1)
    (clear b4)
    (clear b8)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (on b6 b2)
    (on b9 b6)
    (ontable b7)
    (on b4 b7)
    (on b8 b4)
    (ontable b3)
    (on b5 b3)
    (on b1 b5)
  ))
)
