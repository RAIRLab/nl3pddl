(define (problem blocks-prob-3)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
    b6 - block
  )

  (:init
    (ontable b3)
    (ontable b5)
    (ontable b4)
    (ontable b1)
    (ontable b6)
    (ontable b2)
    (clear b3)
    (clear b5)
    (clear b4)
    (clear b1)
    (clear b6)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b6)
    (on b4 b6)
    (on b1 b4)
    (ontable b2)
    (on b5 b2)
    (on b3 b5)
  ))
)
