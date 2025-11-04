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
    (ontable b5)
    (on b7 b5)
    (ontable b3)
    (on b4 b3)
    (ontable b6)
    (ontable b8)
    (clear b1)
    (clear b7)
    (clear b4)
    (clear b6)
    (clear b8)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b3 b6)
    (on b7 b3)
    (on b4 b7)
    (on b5 b4)
    (on b8 b5)
    (on b1 b8)
    (on b2 b1)
  ))
)
