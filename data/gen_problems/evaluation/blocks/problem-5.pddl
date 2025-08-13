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
    (ontable b7)
    (on b4 b7)
    (ontable b2)
    (on b5 b2)
    (ontable b1)
    (on b8 b1)
    (ontable b6)
    (ontable b3)
    (clear b4)
    (clear b5)
    (clear b8)
    (clear b6)
    (clear b3)
    (handempty)
  )

  (:goal (and
    (ontable b2)
    (on b4 b2)
    (on b1 b4)
    (on b3 b1)
    (on b6 b3)
    (on b8 b6)
    (on b5 b8)
    (on b7 b5)
  ))
)
