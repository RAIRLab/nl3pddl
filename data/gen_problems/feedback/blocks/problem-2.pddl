(define (problem blocks-prob-2)
  (:domain blocks)

  (:objects
    b1 - block
    b2 - block
    b3 - block
    b4 - block
    b5 - block
  )

  (:init
    (ontable b5)
    (on b3 b5)
    (ontable b1)
    (ontable b4)
    (ontable b2)
    (clear b3)
    (clear b1)
    (clear b4)
    (clear b2)
    (handempty)
  )

  (:goal (and
    (ontable b3)
    (on b1 b3)
    (on b2 b1)
    (on b4 b2)
    (on b5 b4)
  ))
)
