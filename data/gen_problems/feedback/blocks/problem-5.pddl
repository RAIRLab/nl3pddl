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
    (ontable b5)
    (on b4 b5)
    (ontable b1)
    (on b3 b1)
    (ontable b2)
    (on b7 b2)
    (ontable b8)
    (ontable b6)
    (clear b4)
    (clear b3)
    (clear b7)
    (clear b8)
    (clear b6)
    (handempty)
  )

  (:goal (and
    (ontable b4)
    (on b7 b4)
    (ontable b2)
    (on b5 b2)
    (ontable b1)
    (on b3 b1)
    (ontable b8)
    (on b6 b8)
  ))
)
